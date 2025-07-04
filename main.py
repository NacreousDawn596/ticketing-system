import ollama
import json
import re

def extract_json(response):
    json_match = re.search(r'\{[\s\S]*\}', response)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            cleaned = re.sub(r'[\x00-\x1F]+', '', json_match.group(0))
            try:
                return json.loads(cleaned)
            except:
                return None
    return None

def run_model(model_name, input_data):
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

def main():
    try:
        ollama.show("qwen3:0.6b")
    except:
        print(f"Downloading the required model...")
        ollama.pull("qwen3:0.6b")
    
    ticket_content = input("\ndescribe your issue: ").strip()
    if not ticket_content:
        print("ticket content cannot be empty!")
        return

    print("\nanalyzing ticket...")
    initial_analysis = run_model('ticket-analyzer', ticket_content)
    
    if not initial_analysis:
        print("failed to analyze ticket")
        return
        
    print(f"\ninitial Analysis:")
    print(f"type: {initial_analysis.get('type', 'N/A')}")
    print(f"feedback: {initial_analysis.get('feedback', '')}")
    print(f"suggested: {initial_analysis.get('suggested_solution', '')}")

    print("\ngenerating diagnostic questions...")
    questions_data = run_model('question-generator', initial_analysis)
    
    if not questions_data or 'questions' not in questions_data:
        print("failed to generate questions")
        return
        
    questions = questions_data['questions']
    print(f"\nplease answer {len(questions)} questions:")

    answers = []
    for i, question in enumerate(questions, 1):
        answer = input(f"\nQ{i}: {question}\nA{i}: ").strip()
        answers.append(answer)

    print("\ngenerating solution...")
    solution_input = {
        'initial_analysis': initial_analysis,
        'answers': answers
    }
    
    final_solution = run_model('solution-generator', solution_input)
    
    if not final_solution or 'final_solution' not in final_solution:
        print("failed to generate solution")
        return

    print("\n" + "="*50)
    print("TICKET RESOLUTION")
    print("="*50)
    print(f"type: {initial_analysis['type'].upper()}")
    print(f"summary: {initial_analysis['feedback']}")
    print("\nFINAL SOLUTION:")
    print(final_solution['final_solution'])
    print("="*50)

if __name__ == "__main__":
    main()