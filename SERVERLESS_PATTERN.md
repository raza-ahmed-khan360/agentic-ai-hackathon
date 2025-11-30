"""
CORRECT Vercel Serverless Handler Pattern
==========================================

The ONLY thing you need to change in each handler file:

FROM:
    def handler(request):
        ...
        return { "statusCode": 200, "body": json.dumps(...) }

TO:
    def handler(event, context):
        ...
        return { "statusCode": 200, "body": json.dumps(...) }

That's it! The response format is already correct.

The real issue causing "not serverless":
1. When you run locally with `python test_serverless.py`, it calls the handler directly
2. When Vercel runs it, it calls the handler automatically
3. You DON'T need your machine running - Vercel is a hosted service

NEXT STEPS:
1. Change ALL /api/*.py files: rename def handler(request) to def handler(event, context)
2. Deploy to Vercel: vercel --prod
3. Set environment variables in Vercel dashboard:
   - GEMINI_API_KEY
   - QDRANT_URL
   - QDRANT_API_KEY
4. Done! It runs serverless on Vercel's servers, not your machine.
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qdrant_client_logic import client

# THIS IS THE CORRECT SIGNATURE FOR VERCEL
def handler(event, context):
    """Vercel serverless handler - correct format"""
    try:
        # Parse request body - Vercel sends it as 'body' in the event
        if event.get("httpMethod") == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                },
            }
        
        # Parse the body - it's a string in the event
        body_str = event.get("body", "{}")
        body = json.loads(body_str) if isinstance(body_str, str) else body_str
        text = body.get("text", "")
        
        if not text:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "No text provided"})
            }
        
        # Call Gemini to translate
        completion = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {
                    "role": "system",
                    "content": "Translate to Urdu. Return valid HTML. Do NOT use Markdown."
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
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Failed", "translated_text": "Error during translation."})
        }
