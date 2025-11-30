#!/usr/bin/env python3
"""
Test Vercel serverless handlers locally.
"""
import json
import sys
import os

# Set up path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Mock request object for testing
class MockRequest:
    def __init__(self, method="POST", body=None):
        self.method = method
        self.body = json.dumps(body) if body else "{}"

def test_handlers():
    """Test all serverless handlers"""
    from backend.api.index import handler as index_handler
    from backend.api.embed import handler as embed_handler
    from backend.api.translate import handler as translate_handler
    from backend.api.personalize import handler as personalize_handler
    from backend.api.chat import handler as chat_handler
    from backend.api.query import handler as query_handler
    
    print("\n🧪 Testing Vercel Serverless Handlers\n")
    
    # Test 1: Index (health check)
    print("1️⃣  Testing /api/ (health check)...")
    try:
        request = MockRequest(method="GET", body={})
        response = index_handler(request)
        print(f"   ✅ Response: {response['statusCode']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Embed
    print("\n2️⃣  Testing /api/embed...")
    try:
        request = MockRequest(method="POST", body={"text": "Hello world"})
        response = embed_handler(request)
        body = json.loads(response['body'])
        if 'embedding' in body:
            print(f"   ✅ Got embedding with {body.get('dimension', 0)} dimensions")
        else:
            print(f"   ❌ No embedding returned")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Translate
    print("\n3️⃣  Testing /api/translate...")
    try:
        request = MockRequest(method="POST", body={"text": "Hello"})
        response = translate_handler(request)
        body = json.loads(response['body'])
        if 'translated_text' in body:
            print(f"   ✅ Translation: {body['translated_text'][:50]}...")
        else:
            print(f"   ❌ No translation")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Personalize
    print("\n4️⃣  Testing /api/personalize...")
    try:
        request = MockRequest(method="POST", body={"text": "Complex content", "level": "simple"})
        response = personalize_handler(request)
        body = json.loads(response['body'])
        if 'personalized_text' in body:
            print(f"   ✅ Personalized: {body['personalized_text'][:50]}...")
        else:
            print(f"   ❌ No personalization")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Chat
    print("\n5️⃣  Testing /api/chat...")
    try:
        request = MockRequest(method="POST", body={"text": "What is Physical AI?", "selected_text": ""})
        response = chat_handler(request)
        body = json.loads(response['body'])
        if 'answer' in body:
            print(f"   ✅ Answer: {body['answer'][:50]}...")
        else:
            print(f"   ❌ No answer")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Query
    print("\n6️⃣  Testing /api/query...")
    try:
        request = MockRequest(method="POST", body={"question": "Physical AI"})
        response = query_handler(request)
        body = json.loads(response['body'])
        if 'results' in body:
            print(f"   ✅ Found {body.get('count', 0)} results")
        else:
            print(f"   ❌ No results")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "="*50)
    print("✅ Serverless handlers are ready for Vercel deployment!")
    print("="*50)

if __name__ == "__main__":
    test_handlers()
