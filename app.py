import logging
import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from ollama import ResponseError
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse

from config.logging_config import configure_logging
from models.schemas import QuestionRequest, QuestionResponse
from rag.pipeline import ask
from vector_db.qdrant_store import create_client

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Created once per server process (not at import time) so the reload
    # watcher process never opens the local Qdrant storage folder.
    app.state.qdrant_client = create_client()
    yield
    app.state.qdrant_client.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_qdrant_client(request: Request) -> QdrantClient:
    return request.app.state.qdrant_client


@app.get("/")
def home():
    return {
        "message": "University RAG API is running!"
    }


def _log_ask_failed(error, start):
    total_time_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.error(
        "ask_failed",
        extra={
            "event": "ask_failed",
            "status": "error",
            "error_type": type(error).__name__,
            "total_time_ms": total_time_ms,
        },
    )


@app.post("/ask", response_model=QuestionResponse)
def ask_question(
    request: QuestionRequest,
    qdrant_client: QdrantClient = Depends(get_qdrant_client),
):
    start = time.perf_counter()

    logger.info(
        "ask_received",
        extra={"event": "ask_received", "question_length": len(request.question)},
    )

    try:
        result = ask(request.question, qdrant_client)
    except UnexpectedResponse as e:
        _log_ask_failed(e, start)
        raise HTTPException(status_code=503, detail=f"Retrieval backend unavailable: {e}")
    except (ConnectionError, ResponseError) as e:
        _log_ask_failed(e, start)
        raise HTTPException(status_code=503, detail=f"LLM backend unavailable: {e}")
    except Exception as e:
        _log_ask_failed(e, start)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    total_time_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info(
        "ask_completed",
        extra={
            "event": "ask_completed",
            "status": "success",
            "total_time_ms": total_time_ms,
        },
    )

    return result