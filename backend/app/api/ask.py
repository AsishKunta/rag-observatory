"""Question answering endpoint for engineering knowledge queries."""

from fastapi import APIRouter
from app.models.document import AnswerResponse, QuestionRequest
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService

router = APIRouter()
retrieval_service = RetrievalService()
llm_service = LLMService()

@router.post("/ask", response_model=AnswerResponse, tags=["ask"])
async def ask_question(payload: QuestionRequest):
    """Accept a question and return a generated answer grounded in retrieved context."""
    # Step 1: Retrieve relevant document chunks
    retrieval_results = retrieval_service.search_semantic(payload.question)
    matches = retrieval_results.get("matches", [])
    confidence = retrieval_results.get("confidence", 0.0)
    sources = list(dict.fromkeys(match["source"] for match in matches))

    # Step 2: Combine retrieved chunks into context for LLM
    context = "\n\n".join(match["content"] for match in matches) if matches else ""

    # Step 3: Generate answer using LLM with context
    retrieval_type = "semantic"
    answer = "No relevant content found."

    if context:
        generated_answer = llm_service.generate_answer(payload.question, context)
        if generated_answer:
            answer = generated_answer
            retrieval_type = "semantic+llm"
        else:
            # Fallback: use first retrieved chunk if LLM is unavailable
            answer = matches[0]["content"] if matches else "No relevant content found."
            retrieval_type = "semantic"

    return AnswerResponse(
        answer=answer,
        sources=sources,
        retrieval=retrieval_type,
        confidence=confidence,
    )
