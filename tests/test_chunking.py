from ingestion.pdf_loader import load_pdf
from ingestion.chunker import chunk_text

text = load_pdf("data/lecture_5.pdf")
chunks = chunk_text(text)

print(f"Number of chunks: {len(chunks)}")

print("\nFIRST CHUNK\n")
print(chunks[0])

print("\nSECOND CHUNK\n")
print(chunks[1])