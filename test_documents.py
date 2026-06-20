from ingestion.document_loader import load_documents

documents = load_documents()

print(f"Documents loaded: {len(documents)}")

for doc in documents:

    print("\n---------------------")
    print(doc["source"])
    print(doc["type"])
    print(f"Characters: {len(doc['text'])}")