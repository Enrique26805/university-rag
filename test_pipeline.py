from rag.pipeline import ask

result = ask("What is self-attention?")

print("\nAnswer:\n")
print(result["answer"])

print("\nSources:")
for source in result["sources"]:
    print(f"- {source}")