from ingestion.document_loader import load_documents
from ingestion.chunk_documents import chunk_documents

documents = load_documents()

chunks = chunk_documents(documents)

print(f"Documents: {len(documents)}")
print(f"chunks: {len(chunks)}")

print("\nSample Chunks:\n")

print(chunks[0]["source"])
print(chunks[0]["chunk_id"])

print(chunks[0]["text"][:500])