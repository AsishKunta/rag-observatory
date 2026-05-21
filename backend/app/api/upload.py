"""Document upload endpoint for engineering PDF ingestion."""

import os
from fastapi import APIRouter, File, HTTPException, UploadFile
from backend.app.models.document import UploadResponse
from backend.app.services.document_service import DocumentService

router = APIRouter()
service = DocumentService()

@router.post("/upload", response_model=UploadResponse, tags=["upload"])
async def upload_document(file: UploadFile = File(...)):
    """Persist an uploaded PDF file to local storage."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported.")

    save_path = service.save_pdf(file.filename, await file.read())
    return UploadResponse(file_name=os.path.basename(save_path), message="PDF uploaded successfully.")
