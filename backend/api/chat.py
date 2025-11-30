import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qdrant_client_logic import client, qdrant, COLLECTION_NAME, embed_text

def handler(event, context):
    """Vercel serverless handler for /api/chat - RAG endpoint"""
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
        question_text = body.get("text", "")
        selected_text = body.get("selected_text", "")
        
        if not question_text:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No question provided"})
            }
        
        context = ""
        
        # Retrieval: Use RAG if no selected text
        if not selected_text:
            try:
                # Embed the question
                embedding = embed_text(question_text)
                
                # Search Qdrant
                search_result = qdrant.search(
                    collection_name=COLLECTION_NAME,
                    query_vector=embedding,
                    limit=5
                )
                
                print(f"Found {len(search_result)} chunks.")
                
                # Build context from search results
                for res in search_result:
                    if hasattr(res, 'payload'):
                        context += res.payload.get('text', '') + "\n\n"
                    elif isinstance(res, dict):
                        context += res.get('text', '') + "\n\n"
            
            except Exception as e:
                print(f"Retrieval error: {e}")
                context = ""  # Fallback to empty context
        else:
            context = selected_text
        
        # System instruction for RAG
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
        
        # Generation
        completion = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"[CONTEXT]:\n{context}\n\n[USER QUESTION]: {question_text}"}
            ]
        )
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({
                "answer": completion.choices[0].message.content
            })
        }
    
    except Exception as e:
        print(f"Chat error: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({
                "error": "Chat failed",
                "answer": "I encountered an error. Please try again."
            })
        }
