import os
import traceback
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

class TranslationRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "Agentic AI Backend is Running"}

# --- Personalization Endpoint ---
@app.post("/personalize")
def personalize_endpoint(request: PersonalizeRequest):
    print(f"Personalizing...")
    prompt_style = "Explain simply." if request.level == "simple" else "Explain deeply."
    
    try:
        completion = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                # UPDATED PROMPT: Request HTML
                {"role": "system", "content": f"You are a tutor. {prompt_style} Return the response as valid HTML code (using <h1>, <p>, <ul>, etc). Do NOT use Markdown."},
                {"role": "user", "content": request.text[:6000]}
            ]
        )
        return {"personalized_text": completion.choices[0].message.content}
    except Exception as e:
        traceback.print_exc()
        return {"personalized_text": "Error during personalization."}

@app.post("/translate")
def translate_endpoint(request: TranslationRequest):
    print("Translating...")
    try:
        completion = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                # UPDATED PROMPT: Request HTML
                {"role": "system", "content": "Translate to Urdu. Return the response as valid HTML code (using <h1>, <p>, <ul>, etc). Ensure RTL direction is respected. Do NOT use Markdown."},
                {"role": "user", "content": request.text[:6000]}
            ]
        )
        return {"translated_text": completion.choices[0].message.content}
    except Exception as e:
        traceback.print_exc()
        return {"translated_text": "Error during translation."}

# --- Chat/RAG Endpoint ---
@app.post("/chat")
def chat_endpoint(question: Question):
    print(f"Chat Question: {question.text}")
    context = ""
    
    # 1. Retrieval
    if not question.selected_text:
        try:
            # Embed the question
            emb_response = client.embeddings.create(
                input=question.text,
                model="text-embedding-004"
            )
            embedding = emb_response.data[0].embedding
            
            # Search Qdrant with a LOWER threshold (or no threshold)
            search_result = qdrant.search(
                collection_name=COLLECTION_NAME,
                query_vector=embedding,
                limit=5  # Get MORE context (5 chunks instead of 3)
            )
            
            print(f"Found {len(search_result)} chunks.") # Debug print
            
            for res in search_result:
                # Add the text to the context
                context += res.payload['text'] + "\n\n"
                
        except Exception as e:
            print(f"Retrieval Error: {e}")
            context = "" # Fallback to empty context
    else:
        context = question.selected_text

    # 2. Construction of the System Prompt
    # This is the critical part. We tell the AI how to behave.
    system_instruction = """
    You are an expert Professor for the 'Physical AI & Humanoid Robotics' course.
    Your goal is to help students understand the textbook.
    
    INSTRUCTIONS:
    1. Use the provided [CONTEXT] to answer the user's question.
    2. If the [CONTEXT] contains the answer, explain it clearly.
    3. If the [CONTEXT] is empty or irrelevant, DO NOT say "I cannot answer". 
       Instead, answer based on your general knowledge about Robotics, ROS 2, and AI, 
       but mention: "This specific detail isn't in the current chapter context, but generally..."
    """

    # 3. Generation
    try:
        completion = client.chat.completions.create(
            model="gemini-2.5-flash", 
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"[CONTEXT]:\n{context}\n\n[USER QUESTION]: {question.text}"}
            ]
        )
        return {"answer": completion.choices[0].message.content}
    except Exception as e:
        traceback.print_exc()
        return {"answer": "I encountered an error. Check terminal for details."}