"""Question answering endpoint for engineering knowledge queries."""

from fastapi import APIRouter, HTTPException
from backend.app.models.document import AnswerResponse, QuestionRequest
from backend.app.services.citation_service import CitationService
from backend.app.services.document_service import DocumentService
from backend.app.services.retrieval_service import RetrievalService

router = APIRouter()

document_service = DocumentService()
retrieval_service = RetrievalService()
citation_service = CitationService()

@router.post("/ask", response_model=AnswerResponse, tags=["ask"])
async def ask_question(payload: QuestionRequest):
    """Accept a question and return a grounded answer with source citations."""
    if not document_service.has_documents():
        raise HTTPException(status_code=404, detail="No documents available. Upload PDFs first.")

    chunks = retrieval_service.retrieve(query=payload.question)
    answer = citation_service.build_answer(query=payload.question, chunks=chunks)
    sources = citation_service.format_sources(chunks)

    return AnswerResponse(answer=answer, sources=sources)
