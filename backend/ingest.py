import os
import glob
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from openai import OpenAI 
import uuid

load_dotenv()

# --- CONFIGURATION FOR ZERO COST (GEMINI VIA OPENAI COMPATIBILITY) ---
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),  # Use your Google Key
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # <--- THE TRICK
)

qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

DOCS_PATH = "../docs"
COLLECTION_NAME = "book_chunks"

def ingest_book():
    print("--- Starting Compliance Ingestion (OpenAI SDK -> Gemini) ---")
    
    # 768 is the dimension for Gemini's text-embedding-004
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )
    
    files = glob.glob(os.path.join(DOCS_PATH, "**/*.md"), recursive=True)
    points = []

    for file_path in files:
        print(f"Reading: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                chunks = content.split("\n\n")
                
                for chunk in chunks:
                    if len(chunk) < 50: continue
                    
                    # USE OPENAI SDK TO CALL GEMINI EMBEDDINGS
                    response = client.embeddings.create(
                        input=chunk,
                        model="text-embedding-004"
                    )
                    embedding = response.data[0].embedding
                    
                    points.append(PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embedding,
                        payload={"text": chunk, "source": os.path.basename(file_path)}
                    ))
        except Exception as e:
            print(f"Skipped {file_path}: {e}")

    if points:
        qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f"SUCCESS! {len(points)} chunks uploaded via OpenAI SDK.")

if __name__ == "__main__":
    ingest_book()