"""Document upload endpoint for engineering PDF ingestion."""

import os
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.models.document import UploadResponse
from app.services.document_service import DocumentService, InvalidUploadError

router = APIRouter()
service = DocumentService()

@router.post("/upload", response_model=UploadResponse, tags=["upload"])
async def upload_document(file: UploadFile = File(...)):
    """Persist an uploaded PDF file to local storage and extract text."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported.")

    try:
        save_path = service.save_pdf(file.filename, await file.read())
    except InvalidUploadError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    processed = service.extract_text_from_pdf(save_path)

    return UploadResponse(
        filename=os.path.basename(save_path),
        status="processed",
        pages=processed["pages"],
        characters=processed["characters"],
    )
