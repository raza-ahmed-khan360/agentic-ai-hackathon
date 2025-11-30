import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import QdrantClient
from openai import OpenAI 
from dotenv import load_dotenv

# 1. Initialize Env & Clients LOCALLY (Don't import from ingest)
load_dotenv()

# --- COMPLIANT SETUP (Gemini via OpenAI SDK) ---
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
COLLECTION_NAME = "book_chunks"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---
class Question(BaseModel):
    text: str
    selected_text: str = ""

class PersonalizeRequest(BaseModel):
    text: str
    level: str 

@app.get("/")
def home():
    return {"status": "Agentic AI Backend is Running"}

# --- Personalization Endpoint ---
@app.post("/personalize")
def personalize_endpoint(request: PersonalizeRequest):
    print(f"Personalizing for level: {request.level}")
    
    prompt_style = "Explain this like I'm 5 years old. Use simple analogies." if request.level == "simple" else "Explain this like a PhD researcher. Use technical jargon and deep theoretical context."
    
    try:
        completion = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {"role": "system", "content": f"You are an expert tutor. {prompt_style} Keep Markdown formatting. Do not change code blocks."},
                {"role": "user", "content": request.text[:6000]}
            ]
        )
        return {"personalized_text": completion.choices[0].message.content}
    except Exception as e:
        print(f"Error: {e}")
        return {"personalized_text": "Failed to personalize. Check backend console."}

# --- Translation Endpoint (From previous step) ---
class TranslationRequest(BaseModel):
    text: str

@app.post("/translate")
def translate_endpoint(request: TranslationRequest):
    try:
        completion = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {"role": "system", "content": "Translate Markdown to Urdu. Preserve formatting."},
                {"role": "user", "content": request.text[:6000]}
            ]
        )
        return {"translated_text": completion.choices[0].message.content}
    except Exception as e:
        return {"translated_text": "Translation failed."}

# --- Chat/RAG Endpoint ---
@app.post("/chat")
def chat_endpoint(question: Question):
    print(f"User Question: {question.text}")
    context = ""
    
    # 1. RAG Retrieval
    if question.selected_text and len(question.selected_text) > 10:
        context = f"USER SELECTED TEXT:\n{question.selected_text}"
    else:
        try:
            # Embed using Gemini via OpenAI SDK
            emb_response = client.embeddings.create(
                input=question.text,
                model="text-embedding-004"
            )
            embedding = emb_response.data[0].embedding
            
            # Search Qdrant
            search_result = qdrant.search(
                collection_name=COLLECTION_NAME,
                query_vector=embedding,
                limit=3
            )
            for res in search_result:
                context += res.payload['text'] + "\n\n"
        except Exception as e:
            print(f"Search Error: {e}")
            context = "No context found (Database might be empty)."

    # 2. Generation
    try:
        completion = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {"role": "system", "content": "You are a tutor for the Physical AI course. Answer based ONLY on the context provided."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question.text}"}
            ]
        )
        return {"answer": completion.choices[0].message.content}
    except Exception as e:
        return {"answer": "I encountered an error generating the response."}