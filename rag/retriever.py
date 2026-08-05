import logging
import time

from embeddings.embedder import embed_text
from config.settings import TOP_K

from vector_db.qdrant_store import (
    client,
    COLLECTION_NAME
)

logger = logging.getLogger(__name__)


def retrieve_context(question, top_k=TOP_K):

    start = time.perf_counter()

    query_embedding = embed_text(question)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding.tolist(),
        limit=top_k
    )

    retrieval_time_ms = round((time.perf_counter() - start) * 1000, 2)
    chunks_retrieved = len(results.points)
    top_score = results.points[0].score if chunks_retrieved else None

    logger.info(
        "retrieval_completed",
        extra={
            "event": "retrieval_completed",
            "retrieval_time_ms": retrieval_time_ms,
            "chunks_retrieved": chunks_retrieved,
            "top_score": top_score,
        },
    )

    return results.points