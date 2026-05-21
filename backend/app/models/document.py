"""Data models for document upload, question answering, and health responses."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


class UploadResponse(BaseModel):
    filename: str
    status: str


class QuestionRequest(BaseModel):
    question: str


class SourceItem(BaseModel):
    title: str
    location: str
    excerpt: str | None = None


class AnswerResponse(BaseModel):
    answer: str
    sources: list[SourceItem]
