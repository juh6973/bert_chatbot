# bert_chatbot
BERT chatbot for comp.cs.530 exercise 3

## Setup
1. Generate an API key here: https://console.groq.com/keys
2. Save it as an environment variable `export GROQ_API_KEY=<your-api-key-here>`
3. Install necessary libraries: `pip install -r requirements.txt`

## Run:
- run API first `uvicorn api:app --host 0.0.0.0 --port 8000 --reload`
- run UI `python ui.py`