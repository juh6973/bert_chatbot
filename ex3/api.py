import json
import os
import torch
import torch.nn.functional as F
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from groq import Groq

# Define templates
LABELS = {0: "negative", 1: "positive"}
class SentimentRequest(BaseModel):
    text: str
    model: str

# Initialize FastAPI app
app = FastAPI()

# Initialize Croq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Load the custom fine-tuned model
repo_name = "Juh6973/imdb-distilbert"
custom_model = DistilBertForSequenceClassification.from_pretrained(repo_name, subfolder="imdb_model")
custom_tokenizer = DistilBertTokenizer.from_pretrained(repo_name, subfolder="imdb_tokenizer")

# Define llama variables
llama_model = "llama-3.3-70b-versatile"
system_prompt = "You are a data analyst API capable of sentiment analysis that responds in JSON. The JSON schema should be strictly {\"sentiment_analysis\": {\"sentiment\": \"string (positive, negative, neutral)\", \"confidence_score\": \"number (0-1)\"}}"

# API Endpoint
@app.post("/analyze/")
async def analyze_sentiment(request: SentimentRequest):
    
    if request.model == "custom":
        model, tokenizer = custom_model, custom_tokenizer
        inputs = tokenizer(request.text, return_tensors="pt", truncation=True, max_length=256)

        # Perform inference
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probs = F.softmax(logits, dim=1)
            confidence, predicted_label = torch.max(probs, dim=1)

        return {
            "sentiment_analysis": {
                "sentiment": LABELS[predicted_label.item()],
                "confidence_score": confidence.item()
            }
        } 
    
    elif request.model == "llama":
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.text},
        ]

        chat_completion = client.chat.completions.create(messages=messages, model=llama_model)
        response = chat_completion.choices[0].message.content
        
        return json.loads(response)
    
    else:
        return {"error": "Invalid model name. Use 'custom' or 'llama'."}