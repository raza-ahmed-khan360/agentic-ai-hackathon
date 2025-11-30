#!/usr/bin/env python3
"""
Fix all Vercel serverless handlers to use correct signature.
Changes: def handler(request) -> def handler(event, context)
Also: request.method -> event.get("httpMethod")
      request.body -> event.get("body", "{}")
"""

import os
import re

BACKEND_DIR = os.path.join(os.path.dirname(__file__), "backend", "api")

HANDLER_FILES = [
    "translate.py",
    "personalize.py",
    "chat.py",
    "query.py",
    "embed.py",
    "index.py",
]

def fix_handler(filepath):
    """Fix a handler file to use Vercel signature"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Fix 1: Change function signature
    content = re.sub(
        r'def handler\(request\)',
        'def handler(event, context)',
        content
    )
    
    # Fix 2: Change method check
    content = re.sub(
        r'request\.method\s*==\s*["\']OPTIONS["\']',
        'event.get("httpMethod") == "OPTIONS"',
        content
    )
    
    # Fix 3: Change body parsing
    content = re.sub(
        r'request\.body',
        'event.get("body", "{}")',
        content
    )
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✅ Fixed: {os.path.basename(filepath)}")
        return True
    else:
        print(f"⚠️  No changes needed: {os.path.basename(filepath)}")
        return False

if __name__ == "__main__":
    print("\n🔧 Fixing Vercel serverless handlers...\n")
    
    fixed_count = 0
    for handler_file in HANDLER_FILES:
        filepath = os.path.join(BACKEND_DIR, handler_file)
        if os.path.exists(filepath):
            if fix_handler(filepath):
                fixed_count += 1
        else:
            print(f"❌ Not found: {handler_file}")
    
    print(f"\n✅ Fixed {fixed_count} handlers")
    print("\nNow deploy with: cd backend && vercel --prod")
