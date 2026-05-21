"""Citation service for formatting grounded sources and answers."""

from typing import Any


class CitationService:
    def build_answer(self, query: str, chunks: list[dict[str, Any]]) -> str:
        """Build a placeholder answer from retrieved chunks."""
        # Future implementation: synthesize an answer from chunk content and citation metadata.
        return "This is a starter example answer. Actual answer generation will be implemented with retrieval and grounding logic."

    def format_sources(self, chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Convert retrieved chunks into structured source metadata."""
        return [
            {
                "title": chunk.get("title", "Unknown document"),
                "location": chunk.get("location", "unknown"),
                "excerpt": chunk.get("excerpt", ""),
            }
            for chunk in chunks
        ]
