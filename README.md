# AI Ticketing System

![ticketing system Demo](demo.mp4)

## Overview

This Ticketing System is a sophisticated ticket resolution system that leverages Large Language Models (LLMs) to analyze user issues, generate clarifying questions, and provide actionable solutions. This application implements a multi-stage workflow where:

1. Users describe their technical issues
2. The AI analyzes the problem and categorizes it
3. The system generates diagnostic questions to clarify the issue
4. Based on user responses, the AI provides a tailored solution

The system uses WebSockets for real-time communication and features a sleek, Google-inspired interface with smooth transitions between steps.

## Key Features

- **AI-Powered Ticket Analysis**: Leverages Ollama LLMs for intelligent issue classification
- **Interactive Question Flow**: Dynamic question generation based on initial analysis
- **Real-Time Communication**: WebSocket-based architecture for seamless interactions
- **Modern UI**: Clean, responsive interface with smooth animations
- **Solution Export**: Ability to download solutions as text files

## Requirements
- Python 3.8+
- [Ollama](https://ollama.com/) installed and running
- Required Python packages: `flask`, `flask-socketio`, `ollama` and `sqlite3`

## Setup Instructions

### 1. Clone the Repo:
```bash
git clone https://github.com/NacreousDawn596/ticketing-system.git
cd ticketing-system
```

### 2. Create Ollama models from modelfiles
```bash
# Create ticket analyzer model
ollama create ticket-analyzer -f model.init

# Create question generator model
ollama create question-generator -f model.question

# Create solution generator model
ollama create solution-generator -f model.solution
```

### 3. Install Python dependencies
```bash
pip install flask flask-socketio ollama # or simply nix-shell
```

## Running the Application
### Start the Backend Server
```bash
python backend.py
```

The application will be accessible at [the localhost](http://localhost:5000)

### 2. Describe Your Issue
- Enter a detailed description of your technical problem in the text area
- Example descriptions:
  - "I can't connect to the company VPN after updating to Windows 11"
  - "My application crashes when I try to export PDF files"
  - "Email attachments are failing to send through Outlook"
- Click "Analyze Issue" to begin processing

### 3. Analysis Phase
- The AI will analyze your issue in real-time
- Visual indicators show the system:
  - Identifying key components of your issue
  - Categorizing the problem type
  - Determining the solution approach
- This typically takes 15-30 seconds depending on complexity

### 4. Answer Diagnostic Questions
- The system generates clarifying questions based on your issue
- Example questions you might see:
  - "What specific error message appears when the problem occurs?"
  - "When did you first notice this issue happening?"
  - "Does the problem occur consistently or intermittently?"
- Provide detailed answers for best results
- Navigate between questions using "Back" and "Next Question" buttons

### 5. Receive Your Solution
After answering all questions:
- The AI generates a comprehensive solution including:
  - **Issue Type**: Problem classification (e.g., Network Configuration, Software Conflict)
  - **Technical Analysis**: Explanation of root causes
  - **Recommended Solution**: Step-by-step resolution instructions
- Solution screen options:
  - Download solution as a text file
  - Start over with a new issue

### 6. Download Solution (Optional)
- Click "Download Solution" to save troubleshooting steps
- The text file contains:
  - Timestamp of solution generation
  - Issue classification
  - Technical analysis
  - Actionable resolution steps
  - Recommended follow-up actions

## Troubleshooting

### Common Issues
- **Models not loading**:  
  Ensure you've installed required Ollama models with:  
  `ollama pull qwen3:0.6b`

- **WebSocket connection errors**:  
  Verify no firewall is blocking port 5000  
  Ensure no other service is using port 5000

- **Slow response times**:  
  Reduce other system resource usage  
  Consider hardware upgrades for AI workloads

- **Blank question screen**:  
  Refresh browser and resubmit ticket  
  Verify backend server is running

### Advanced Tips
- For complex issues:
  - Include error codes in initial description
  - Note recent system changes in answers
- If solution is ineffective:
  - Restart process with more detailed description
  - Provide alternative answers to diagnostic questions
- For enterprise use:
  - Increase `num_predict` in backend.py for detailed solutions
  - Add custom prompt engineering in run_model()

## Contributing

We welcome contributions to enhance the AI Support Assistant! Here's how you can help:

### How to Contribute

1. **Fork the Repository**  
   Start by forking the [ticketing system](https://github.com/nacreousdawn596/ticketing-system) repository

2. **Set Up Development Environment**
   git clone https://github.com/nacreousdawn596/ticketing-system.git
   cd ticketing-system
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. **Create a Feature Branch**
   git checkout -b feature/your-feature-name

4. **Make Your Changes**
   - Backend: Modify app.py for server logic
   - Frontend: Update index.html for UI changes
   - Models: Experiment with different Ollama models

5. **Test Your Changes**
   Start the development server:
   python app.py
   Verify your changes work as expected at http://localhost:5000

6. **Commit and Push**
   git add .
   git commit -m "Description of your changes"
   git push origin feature/your-feature-name

7. **Submit a Pull Request**
   Create a PR from your feature branch to the main repository

### Development Guidelines
- Follow PEP 8 for Python code
- Use descriptive commit messages
- Maintain consistent Vue.js component structure
- Keep UI responsive across all device sizes
- Document new features in README
- Add comments for complex logic sections

### Areas Needing Contribution
- Improved error handling
- Additional model integrations
- Enhanced UI animations
- Accessibility improvements
- Localization support
- Performance optimizations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Special thanks to:
- Ollama team for their powerful LLM infrastructure
- Flask and Socket.IO for backend services
- Vue.js and Tailwind CSS for the frontend framework
- sqlite3 for reliable logging and data storage
- The open-source community for inspiration and support

---

**Happy troubleshooting!** If you encounter any issues with the setup or usage, please open an issue on GitHub. We appreciate your contributions to make this project better!