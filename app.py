import logging
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ollama import ResponseError
from qdrant_client.http.exceptions import UnexpectedResponse

from config.logging_config import configure_logging
from models.schemas import QuestionRequest, QuestionResponse
from rag.pipeline import ask

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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
def ask_question(request: QuestionRequest):
    start = time.perf_counter()

    logger.info(
        "ask_received",
        extra={"event": "ask_received", "question_length": len(request.question)},
    )

    try:
        result = ask(request.question)
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