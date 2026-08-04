from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ollama import ResponseError
from qdrant_client.http.exceptions import UnexpectedResponse

from models.schemas import QuestionRequest, QuestionResponse
from rag.pipeline import ask

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


@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):

    try:
        result = ask(request.question)
    except UnexpectedResponse as e:
        raise HTTPException(status_code=503, detail=f"Retrieval backend unavailable: {e}")
    except (ConnectionError, ResponseError) as e:
        raise HTTPException(status_code=503, detail=f"LLM backend unavailable: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    return result