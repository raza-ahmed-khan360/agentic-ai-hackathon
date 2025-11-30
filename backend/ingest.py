import os
import glob
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from openai import OpenAI
import uuid

# 1. Load your keys
load_dotenv()

# 2. Configuration
# NOTE: This assumes ingest.py is in 'backend/' and docs are in 'docs/' (one level up)
DOCS_PATH = "../docs" 
COLLECTION_NAME = "book_chunks"

# 3. Connect to Clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"), 
    api_key=os.getenv("QDRANT_API_KEY")
)

def ingest_book():
    print("--- Starting Ingestion ---")
    
    # 4. Wipe the database clean (so we don't have duplicate chapters)
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )
    print("Database cleared. Reading new files...")

    points = []
    
    # 5. Read every Markdown file in the docs folder
    files = glob.glob(os.path.join(DOCS_PATH, "**/*.md"), recursive=True)
    
    for file_path in files:
        print(f"Reading: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Simple Splitting: Split by double newlines (paragraphs)
                chunks = content.split("\n\n")
                
                for chunk in chunks:
                    # Skip empty lines or very short headings
                    if len(chunk) < 50: continue 
                    
                    # 6. Convert Text to Numbers (Embedding)
                    embedding = client.embeddings.create(
                        input=chunk,
                        model="text-embedding-3-small"
                    ).data[0].embedding
                    
                    # 7. Prepare for Upload
                    points.append(PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embedding,
                        payload={
                            "text": chunk, 
                            "source": os.path.basename(file_path)
                        }
                    ))
                    
        except Exception as e:
            print(f"Skipping file {file_path} due to error: {e}")

    # 8. Upload Everything
    if points:
        print(f"Uploading {len(points)} text chunks to Qdrant...")
        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        print("SUCCESS! The book is now in the AI's brain.")
    else:
        print("WARNING: No valid text found in /docs folder!")

if __name__ == "__main__":
    ingest_book()