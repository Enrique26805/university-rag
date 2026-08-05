from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL

_model = None


def get_embedding_model():
    """Lazily create and cache the embedding model on first use."""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def embed_text(text):

    """
    Convert text to embedding vector.
    """
    embedding = get_embedding_model().encode(text)

    return embedding