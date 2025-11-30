from qdrant_client_logic import embed_text

def handler(request):
    body = request.json()
    text = body.get("text")
    return {"embedding": embed_text(text)}
