"""Service layer for document ingestion and local storage."""

import os
from pathlib import Path
from typing import List
from app.config.settings import settings


class DocumentService:
    def save_pdf(self, file_name: str, content: bytes) -> str:
        """Save an uploaded PDF to the local storage directory."""
        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)

        destination = upload_dir / file_name
        with open(destination, "wb") as out_file:
            out_file.write(content)

        return str(destination)

    def list_documents(self) -> List[str]:
        """Return all stored PDF paths for the local backend."""
        upload_dir = Path(settings.upload_dir)
        if not upload_dir.exists():
            return []
        return [str(path) for path in upload_dir.iterdir() if path.suffix.lower() == ".pdf"]

    def has_documents(self) -> bool:
        """Check whether any documents have been uploaded."""
        return len(self.list_documents()) > 0
