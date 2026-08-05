from rag.pipeline import ask
from vector_db.qdrant_store import create_client

client = create_client()
result = ask("What is self-attention?", client)
client.close()

print("\nAnswer:\n")
print(result["answer"])

print("\nSources:")
for source in result["sources"]:
    print(f"- {source}")