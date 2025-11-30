#!/usr/bin/env python3
"""
Backend connectivity test script.
Tests if the backend is reachable and responds to API calls.
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_backend(backend_url):
    """Test backend connectivity."""
    
    print(f"\n🔍 Testing Backend at: {backend_url}\n")
    
    # Test 1: Health check
    print("1️⃣  Testing health endpoint...")
    try:
        response = requests.get(f"{backend_url}/", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Backend is running: {response.json()}")
        else:
            print(f"   ❌ Backend returned {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot reach backend: {e}")
        return False
    
    # Test 2: Chat endpoint
    print("\n2️⃣  Testing /chat endpoint...")
    try:
        response = requests.post(
            f"{backend_url}/chat",
            json={"text": "What is Physical AI?", "selected_text": ""},
            timeout=10
        )
        if response.status_code == 200:
            print(f"   ✅ Chat endpoint works")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Chat returned {response.status_code}")
    except Exception as e:
        print(f"   ❌ Chat test failed: {e}")
    
    # Test 3: Translate endpoint
    print("\n3️⃣  Testing /translate endpoint...")
    try:
        response = requests.post(
            f"{backend_url}/translate",
            json={"text": "Hello world"},
            timeout=10
        )
        if response.status_code == 200:
            print(f"   ✅ Translate endpoint works")
        else:
            print(f"   ❌ Translate returned {response.status_code}")
    except Exception as e:
        print(f"   ❌ Translate test failed: {e}")
    
    # Test 4: Personalize endpoint
    print("\n4️⃣  Testing /personalize endpoint...")
    try:
        response = requests.post(
            f"{backend_url}/personalize",
            json={"text": "Complex content here", "level": "simple"},
            timeout=10
        )
        if response.status_code == 200:
            print(f"   ✅ Personalize endpoint works")
        else:
            print(f"   ❌ Personalize returned {response.status_code}")
    except Exception as e:
        print(f"   ❌ Personalize test failed: {e}")
    
    print("\n" + "="*50)
    print("✅ All tests completed!")
    print("="*50)

if __name__ == "__main__":
    # Default to localhost for development
    backend_url = os.getenv("REACT_APP_BACKEND_URL", "http://127.0.0.1:8000")
    
    # Allow override via command line
    if len(sys.argv) > 1:
        backend_url = sys.argv[1]
    
    test_backend(backend_url)
