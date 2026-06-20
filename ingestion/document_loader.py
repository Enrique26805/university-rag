from pathlib import Path

from ingestion.pdf_loader import load_pdf

def load_documents(data_folder = "data"):
    documents = []
    data_path = Path(data_folder)

    for pdf_file in data_path.rglob("*.pdf"):

        text = load_pdf(str(pdf_file))

        documents.append({
            "source" : str(pdf_file),
            "type" : "pdf",
            "text" : text
        })

    for md_file in data_path.rglob("*.md"):

        with open(md_file,"r",encoding = "utf-8") as f:
            text = f.read()

        documents.append({
            "source": str(md_file),
            "type": "markdown",
            "text": text
        })

    return documents