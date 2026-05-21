"""FastAPI application entry point for the RAG Observatory backend."""

from fastapi import FastAPI

from app.api.routes import router as api_router

app = FastAPI(
    title="RAG Observatory — Engineering Knowledge Assistant",
    description="A portfolio-ready starter backend for engineering document retrieval, question answering, and grounded citation workflows.",
    version="0.1.0"
)

app.include_router(api_router)
