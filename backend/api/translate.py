import json
from qdrant_client_logic import client

def handler(request):
    body = request.json()
    text = body.get("text")

    result = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": "Translate to Urdu."},
            {"role": "user", "content": text}
        ]
    )

    return {
        "translation": result.choices[0].message["content"]
    }
