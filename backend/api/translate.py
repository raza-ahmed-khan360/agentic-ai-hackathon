import json
import sys
import os

# Add parent directory to path so we can import qdrant_client_logic
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qdrant_client_logic import client

def handler(request):
    """Vercel serverless handler for /api/translate"""
    try:
        # Parse request body
        if request.method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                },
            }
        
        body = json.loads(request.body) if isinstance(request.body, str) else request.body
        text = body.get("text", "")
        
        if not text:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No text provided"})
            }
        
        # Call Gemini to translate
        completion = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {
                    "role": "system",
                    "content": "Translate to Urdu. Return the response as valid HTML code (using <h1>, <p>, <ul>, etc). Ensure RTL direction is respected. Do NOT use Markdown."
                },
                {"role": "user", "content": text[:6000]}
            ]
        )
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({
                "translated_text": completion.choices[0].message.content
            })
        }
    
    except Exception as e:
        print(f"Translation error: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({
                "error": "Translation failed",
                "translated_text": "Error during translation."
            })
        }
