"""Question answering endpoint for engineering knowledge queries."""

from fastapi import APIRouter
from app.models.document import AnswerResponse, QuestionRequest
from app.services.retrieval_service import RetrievalService

router = APIRouter()
service = RetrievalService()

@router.post("/ask", response_model=AnswerResponse, tags=["ask"])
async def ask_question(payload: QuestionRequest):
    """Accept a question and return top matching content from processed text files."""
    results = service.search_documents(payload.question)
    matches = results.get("matches", [])

    answer = matches[0]["content"] if matches else "No relevant content found."
    sources = list(dict.fromkeys(match["source"] for match in matches))

    return AnswerResponse(answer=answer, sources=sources)
