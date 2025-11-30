import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qdrant_client_logic import client

def handler(request):
    """Vercel serverless handler for /api/personalize"""
    try:
        # Handle CORS preflight
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
        level = body.get("level", "moderate")
        
        if not text:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No text provided"})
            }
        
        # Determine prompt based on level
        prompt_style = "Explain simply." if level == "simple" else "Explain deeply."
        
        completion = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a tutor. {prompt_style} Return the response as valid HTML code (using <h1>, <p>, <ul>, etc). Do NOT use Markdown."
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
                "personalized_text": completion.choices[0].message.content
            })
        }
    
    except Exception as e:
        print(f"Personalization error: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({
                "error": "Personalization failed",
                "personalized_text": "Error during personalization."
            })
        }
