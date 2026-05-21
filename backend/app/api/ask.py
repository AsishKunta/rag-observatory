"""Question answering endpoint for engineering knowledge queries."""

from fastapi import APIRouter
from app.models.document import AnswerResponse, QuestionRequest

router = APIRouter()

@router.post("/ask", response_model=AnswerResponse, tags=["ask"])
async def ask_question(payload: QuestionRequest):
    """Accept a question and return a placeholder answer."""
    return AnswerResponse(
        answer="Question received. Retrieval not implemented yet.",
        sources=[],
    )
