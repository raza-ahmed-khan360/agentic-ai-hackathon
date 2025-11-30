import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qdrant_client_logic import embed_text

def handler(event, context):
    """Vercel serverless handler for /api/embed - get embeddings"""
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
        text = body.get("text", "")
        
        if not text:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No text provided"})
            }
        
        # Get embedding
        embedding = embed_text(text)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({
                "embedding": embedding,
                "dimension": len(embedding) if embedding else 0
            })
        }
    
    except Exception as e:
        print(f"Embedding error: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({
                "error": "Embedding failed"
            })
        }
