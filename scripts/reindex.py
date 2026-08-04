"""
Drop and rebuild the Qdrant collection from scratch, re-ingesting data/.

Run from the project root:
    python -m scripts.reindex
"""

import sys

from qdrant_client.models import Distance, PointStruct, VectorParams

from config.settings import COLLECTION_NAME
from embeddings.embedder import embed_text
from ingestion.chunk_documents import chunk_documents
from ingestion.document_loader import load_documents
from vector_db.qdrant_store import client

EMBEDDING_SIZE = 384
UPLOAD_BATCH_SIZE = 100


def confirm(collection_name):
    answer = input(
        f"This will permanently delete the '{collection_name}' collection "
        "and rebuild it from data/. Continue? [y/N]: "
    )
    return answer.strip().lower() == "y"


def recreate_collection(collection_name):
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
        print(f"Dropped existing collection '{collection_name}'.")

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE),
    )
    print(f"Created collection '{collection_name}'.")


def reindex(collection_name):
    print("Loading documents...")
    documents = load_documents()

    print("Chunking documents...")
    chunks = chunk_documents(documents)
    print(f"Total chunks: {len(chunks)}")

    if not chunks:
        print("No chunks found in data/ - nothing to index.")
        return

    print("Embedding chunks...")
    points = [
        PointStruct(
            id=i,
            vector=embed_text(chunk["text"]).tolist(),
            payload={
                "text": chunk["text"],
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
            },
        )
        for i, chunk in enumerate(chunks)
    ]

    print("Uploading to Qdrant...")
    for start in range(0, len(points), UPLOAD_BATCH_SIZE):
        batch = points[start : start + UPLOAD_BATCH_SIZE]
        client.upsert(collection_name=collection_name, points=batch)

    print(f"Indexed {len(points)} chunks successfully!")


def main():
    if not confirm(COLLECTION_NAME):
        print("Aborted. No changes were made.")
        sys.exit(0)

    recreate_collection(COLLECTION_NAME)
    reindex(COLLECTION_NAME)
    client.close()


if __name__ == "__main__":
    main()
