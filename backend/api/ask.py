import json
from qdrant_client_logic import client

def handler(request):
    body = request.json()
    question = body.get("question")

    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "user", "content": question}
        ]
    )

    return {
        "answer": response.choices[0].message["content"]
    }
