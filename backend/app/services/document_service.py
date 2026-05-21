"""Service layer for document ingestion and local storage."""

from pathlib import Path
from typing import List
from pypdf import PdfReader
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

    def extract_text_from_pdf(self, file_path: str) -> dict:
        """Extract text from all PDF pages and persist a processed text file."""
        source_path = Path(file_path)
        reader = PdfReader(file_path)
        pages = len(reader.pages)

        extracted_pages = []
        for page in reader.pages:
            text = page.extract_text() or ""
            extracted_pages.append(text)

        full_text = "\n\n".join(extracted_pages).strip()
        processed_dir = Path(settings.upload_dir) / "processed"
        processed_dir.mkdir(parents=True, exist_ok=True)

        target_file = processed_dir / f"{source_path.stem}.txt"
        target_file.write_text(full_text, encoding="utf-8")

        return {
            "filename": target_file.name,
            "pages": pages,
            "characters": len(full_text),
        }

    def list_documents(self) -> List[str]:
        """Return all stored PDF paths for the local backend."""
        upload_dir = Path(settings.upload_dir)
        if not upload_dir.exists():
            return []
        return [str(path) for path in upload_dir.iterdir() if path.suffix.lower() == ".pdf"]

    def has_documents(self) -> bool:
        """Check whether any documents have been uploaded."""
        return len(self.list_documents()) > 0
