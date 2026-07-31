from ingestion.pdf_loader import load_pdf

text = load_pdf("data/lecture_5.pdf")

print(f"Characters: {len(text)}")

print(text[:2000])