from ingestion.document_loader import load_documents
from ingestion.chunk_documents import chunk_documents
from embeddings.embedder import embed_text
from vector_store.qdrant_store import (
    client,
    COLLECTION_NAME
)
from qdrant_client.models import PointStruct

print("Loading documents...")
documents = load_documents()

print("Chunking documents...")
chunks = chunk_documents(documents)

print(f"Total chunks: {len(chunks)}")

points = []

for i, chunk in enumerate(chunks):
    embedding = embed_text(chunk["text"])

    points.append(
        PointStruct(
            id=i,
            vector=embedding.tolist(),
            payload={
                "text": chunk["text"],
                "source": chunk["source"],
                "chunk_id" : chunk["chunk_id"]
                
            }
        )
    )

    print("Uploading to Qdrant...")

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"Indexed {len(points)} chunks successfully!")
