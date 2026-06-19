import fitz
import re

def load_pdf(pdf_path):

    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    text = re.sub(r'\n{2,}','\n',text)
    
    return text