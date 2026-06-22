from embeddings.embedder import embed_text

text = "What problem does ResNet Solve?"

embedding = embed_text(text)

print(type(embedding))
print(f"Vector Length:{len(embedding)}")

print("\nFirst 10 values:\n")
print(embedding[:10])