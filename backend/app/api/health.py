"""Health check endpoint for the RAG Observatory backend."""

from fastapi import APIRouter
from backend.app.models.document import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """Return a simple service health response."""
    return {"status": "healthy"}
