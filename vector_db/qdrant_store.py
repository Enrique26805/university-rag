from qdrant_client import QdrantClient
from config.settings import COLLECTION_NAME

QDRANT_PATH = "qdrant_storage"


def create_client():
    """Create a new QdrantClient. Local on-disk storage is file-locked, so
    each process should call this exactly once (e.g. app startup or a
    standalone script) rather than sharing a module-level instance.
    """
    return QdrantClient(path=QDRANT_PATH)

