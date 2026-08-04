from pydantic import BaseModel, Field
from typing import List


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1)


class Source(BaseModel):
    document: str
    score: float


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]
    retrieved_chunks: int