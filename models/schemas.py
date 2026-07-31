from pydantic import BaseModel
from typing import List


class QuestionRequest(BaseModel):
    question: str


class Source(BaseModel):
    document: str
    score: float


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]
    retrieved_chunks: int