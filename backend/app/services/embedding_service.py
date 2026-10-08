"""Embedding service for generating and caching semantic representations."""

from typing import Optional
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Singleton embedding service with in-memory caching."""

    _instance: Optional["EmbeddingService"] = None
    _model: Optional[SentenceTransformer] = None

    def __new__(cls) -> "EmbeddingService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._model is None:
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
        self._cache: dict[str, list[float]] = {}

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for texts, using cache when available.

        Returns one embedding per input text, in input order. Only texts not
        already cached are sent to the model, and duplicates are encoded once.
        """
        # dict.fromkeys de-duplicates while preserving first-seen order.
        missing = [text for text in dict.fromkeys(texts) if text not in self._cache]

        if missing:
            new_embeddings = self._model.encode(missing, convert_to_numpy=True).tolist()
            self._cache.update(zip(missing, new_embeddings))

        return [self._cache[text] for text in texts]

    def clear_cache(self) -> None:
        """Clear the embedding cache."""
        self._cache.clear()
