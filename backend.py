import ollama
import json
import re
import sqlite3
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
from uuid import uuid4
from datetime import datetime

app = Flask(__name__, template_folder='./')
app.config['SECRET_KEY'] = 'MounaIsTheBest'
socketio = SocketIO(app, cors_allowed_origins="*")
app.config['SESSION_TYPE'] = 'filesystem'

# --- Logging Setup ---
DB_PATH = 'logs.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            event TEXT,
            data TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_event(session_id, event, data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'INSERT INTO logs (session_id, event, data, timestamp) VALUES (?, ?, ?, ?)',
        (session_id, event, json.dumps(data), datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

init_db()
# --- End Logging Setup ---

def extract_json(response):
    json_matches = list(re.finditer(r'\{[\s\S]*?\}', response))
    if json_matches:
        last_json = json_matches[-1].group(0)
        try:
            return json.loads(last_json)
        except json.JSONDecodeError:
            cleaned = re.sub(r'[\x00-\x1F]+', '', last_json)
            try:
                return json.loads(cleaned)
            except:
                return None
    return None

def run_model(model_name, input_data):
    """Run an Ollama model and extract JSON from response"""
    try:
        if isinstance(input_data, dict):
            prompt = json.dumps(input_data)
        else:
            prompt = input_data

        response = ollama.generate(
            model=model_name,
            prompt=prompt,
            options={'num_predict': 512, 'temperature': 0.1}
        )
        return extract_json(response['response'].strip())
    except Exception as e:
        print(f"Model error: {e}")
        return None

@app.route('/')
def index():
    session_id = str(uuid4())
    session['session_id'] = session_id
    return render_template('index.html', session_id=session_id)

sessions = {}

@socketio.on('analyze_ticket')
def handle_ticket_analysis(json_data):
    ticket_content = json_data['ticket_content']
    session_id = json_data['session_id']

    sessions[session_id] = {
        'ticket_content': ticket_content,
        'current_step': 'analyzing'
    }

    log_event(session_id, 'ticket_received', {'ticket_content': ticket_content})

    emit('analysis_status', {'status': 'started', 'message': '🔍 Analyzing ticket...'})

    initial_analysis = run_model('ticket-analyzer', ticket_content)
    log_event(session_id, 'initial_analysis', {'initial_analysis': initial_analysis})

    if not initial_analysis:
        emit('analysis_error', {'error': 'Failed to analyze ticket'})
        log_event(session_id, 'analysis_error', {'error': 'Failed to analyze ticket'})
        return

    sessions[session_id]['initial_analysis'] = initial_analysis

    questions_data = run_model('question-generator', initial_analysis)
    log_event(session_id, 'questions_generated', {'questions_data': questions_data})

    if not questions_data or 'questions' not in questions_data:
        emit('analysis_error', {'error': 'Failed to generate questions'})
        log_event(session_id, 'analysis_error', {'error': 'Failed to generate questions'})
        return

    sessions[session_id]['questions'] = questions_data['questions']
    sessions[session_id]['answers'] = [""] * len(questions_data['questions'])

    emit('questions_ready', {
        'questions': questions_data['questions'],
        'total_questions': len(questions_data['questions'])
    })

@socketio.on('submit_answer')
def handle_answer_submission(json_data):
    session_id = json_data['session_id']
    question_index = json_data['question_index']
    answer = json_data['answer']

    if session_id not in sessions:
        emit('answer_error', {'error': 'Session expired'})
        log_event(session_id, 'answer_error', {'error': 'Session expired'})
        return

    sessions[session_id]['answers'][question_index] = answer
    log_event(session_id, 'answer_submitted', {
        'question_index': question_index,
        'question': sessions[session_id]['questions'][question_index],
        'answer': answer
    })

    if all(a.strip() for a in sessions[session_id]['answers']):
        emit('solution_status', {'status': 'generating', 'message': '💡 Generating solution...'})

        solution_input = {
            'initial_analysis': sessions[session_id]['initial_analysis'],
            'answers': sessions[session_id]['answers']
        }

        log_event(session_id, 'solution_input', solution_input)

        final_solution = run_model('solution-generator', solution_input)
        log_event(session_id, 'final_solution', {'final_solution': final_solution})

        if not final_solution or 'final_solution' not in final_solution:
            emit('solution_error', {'error': 'Failed to generate solution'})
            log_event(session_id, 'solution_error', {'error': 'Failed to generate solution'})
            return

        emit('solution_ready', {
            'type': sessions[session_id]['initial_analysis'].get('type', 'N/A'),
            'feedback': sessions[session_id]['initial_analysis'].get('feedback', ''),
            'final_solution': final_solution['final_solution']
        })
    else:
        next_index = question_index + 1
        emit('next_question', {
            'question_index': next_index,
            'question': sessions[session_id]['questions'][next_index]
        })

if __name__ == '__main__':
    try:
        ollama.show("qwen3:0.6b")
    except:
        print(f"Downloading the required model...")
        ollama.pull("qwen3:0.6b")

    socketio.run(app, host='0.0.0.0', port=5000, debug=True)