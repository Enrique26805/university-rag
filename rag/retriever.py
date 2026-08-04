from embeddings.embedder import embed_text
from config.settings import TOP_K

from vector_db.qdrant_store import (
    client,
    COLLECTION_NAME
)


def retrieve_context(question, top_k=TOP_K):

    query_embedding = embed_text(question)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding.tolist(),
        limit=top_k
    )

    return results.points