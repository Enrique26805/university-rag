from ingestion.document_loader import load_documents
from ingestion.chunk_documents import chunk_documents
from embeddings.embedder import embed_text
from vector_db.qdrant_store import (
    create_client,
    COLLECTION_NAME
)
from qdrant_client.models import PointStruct

UPLOAD_BATCH_SIZE = 100

client = create_client()

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

for start in range(0, len(points), UPLOAD_BATCH_SIZE):
    batch = points[start : start + UPLOAD_BATCH_SIZE]
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=batch
    )

print(f"Indexed {len(points)} chunks successfully!")

client.close()
