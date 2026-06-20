from ingestion.chunker import chunk_text

def chunk_documents(documents):

    all_chunks = []

    for doc in documents:

        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):

            all_chunks.append({
                "text": chunk,
                "source": doc["source"],
                "type": doc["type"],
                "chunk_id": i
            })

    return all_chunks