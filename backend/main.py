from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

# Initialize App
app = FastAPI()

# Enable CORS (So your Docusaurus frontend can talk to this backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace * with your GitHub Pages URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for the request
class Question(BaseModel):
    text: str
    selected_text: str = "" # For the "selection" feature

@app.get("/")
def home():
    return {"status": "Backend is running"}

@app.post("/chat")
def chat_endpoint(question: Question):
    # TODO: Connect this to Qdrant and OpenAI later
    # This is just the skeleton to prove it works
    
    print(f"Received question: {question.text}")
    
    return {
        "answer": f"I received your question: '{question.text}'. The RAG system is not connected yet, but the API is working!"
    }

# To run this: uvicorn main:app --reload