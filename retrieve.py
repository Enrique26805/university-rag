from embeddings.embedder import embed_text

from vector_store.qdrant_store import (
    client,
    COLLECTION_NAME
)

query = " What is self-attention?"

query_embedding = embed_text(query)

results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_embedding.tolist(),
    limit = 5
)

print("\n Top Results:\n")

for point in results.points:

    print("=" * 80)
    print("Score:", point.score)
    print("Source:", point.payload["source"])
    print()
    print(point.payload["text"][:500])
    print()