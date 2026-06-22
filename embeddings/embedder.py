from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def embed_text(text):

    """
    Convert text to embedding vector.
    """
    embedding = model.encode(text)

    return embedding