from qdrant_client_logic import embed_text, qdrant, COLLECTION_NAME

def handler(request):
    body = request.json()
    question = body.get("question")

    vector = embed_text(question)

    search = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=5
    )

    hits = [hit.payload for hit in search]

    return {"results": hits}
