from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

def embed_text(text):

    """
    Convert text to embedding vector.
    """
    embedding = model.encode(text)

    return embedding