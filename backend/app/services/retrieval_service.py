"""Retrieval service for finding relevant document paragraphs in extracted text files."""

from pathlib import Path
from typing import Any

from app.config.settings import settings


def normalize_text(text: str) -> str:
    """Normalize text for simple keyword matching."""
    return " ".join(text.lower().split())


class RetrievalService:
    def search_documents(self, question: str) -> dict[str, list[dict[str, Any]]]:
        """Search extracted text files and return the top matching paragraphs."""
        processed_dir = Path(settings.upload_dir) / "processed"
        if not processed_dir.exists():
            return {"matches": []}

        query_tokens = set(normalize_text(question).split())
        if not query_tokens:
            return {"matches": []}

        matches: list[dict[str, Any]] = []

        for txt_file in sorted(processed_dir.glob("*.txt")):
            text = txt_file.read_text(encoding="utf-8")
            paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]
            if not paragraphs:
                paragraphs = [line.strip() for line in text.splitlines() if line.strip()]

            for paragraph in paragraphs:
                normalized_paragraph = normalize_text(paragraph)
                paragraph_tokens = normalized_paragraph.split()
                score = sum(1 for token in query_tokens if token in paragraph_tokens)
                matches.append({
                    "score": score,
                    "source": txt_file.name,
                    "content": paragraph,
                })

        matches.sort(key=lambda item: item["score"], reverse=True)
        return {"matches": matches[:3]}
