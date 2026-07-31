from fastapi import FastAPI
from pydantic import BaseModel

from rag.pipeline import ask

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "University RAG API is running!"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    result = ask(request.question)

    return result