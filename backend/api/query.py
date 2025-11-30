import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qdrant_client_logic import qdrant, COLLECTION_NAME, embed_text

def handler(event, context):
    """Vercel serverless handler for /api/query - similarity search"""
    try:
        # Handle CORS preflight
        if event.get("httpMethod") == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                },
            }
        
        body = json.loads(event.get("body", "{}")) if isinstance(event.get("body", "{}"), str) else event.get("body", "{}")
        question = body.get("question", "")
        
        if not question:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No question provided"})
            }
        
        # Embed the question
        vector = embed_text(question)
        
        # Search Qdrant
        search_results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=5
        )
        
        # Extract results
        hits = []
        for hit in search_results:
            if hasattr(hit, 'payload'):
                hits.append(hit.payload)
            elif isinstance(hit, dict):
                hits.append(hit)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({
                "results": hits,
                "count": len(hits)
            })
        }
    
    except Exception as e:
        print(f"Query error: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({
                "error": "Query failed",
                "results": []
            })
        }
from qdrant_client_logic import embed_text, qdrant, COLLECTION_NAME

def handler(event, context):
    body = request.json()
    question = body.get("question")

    vector = embed_text(question)

    search = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=5
    )

    hits = [hit.payload for hit in search]

    return {"results": hits}
