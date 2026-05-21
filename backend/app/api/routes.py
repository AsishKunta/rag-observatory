"""Consolidated API router for the RAG Observatory backend.

This module loads endpoint routers for health, upload, and question answering.
"""

from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.api.ask import router as ask_router

router = APIRouter()
router.include_router(health_router)
router.include_router(upload_router)
router.include_router(ask_router)
