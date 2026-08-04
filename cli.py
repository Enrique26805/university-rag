from embeddings.embedder import embed_text
from generation.generator import generate_answer

from vector_db.qdrant_store import(
    client,
    COLLECTION_NAME
)

question = input("Ask a question: ")

query_embedding = embed_text(question)

results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_embedding.tolist(),
    limit = 3
)

context = ""

for point in results.points:
    context += point.payload["text"]
    context += "\n\n"

prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""
response = generate_answer(prompt)

print("\nAnswer:\n")
print(response)

client.close()