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
        """Generate embeddings for texts, using cache when available."""
        embeddings = []
        texts_to_embed = []
        text_indices = []

        for idx, text in enumerate(texts):
            if text in self._cache:
                embeddings.append((idx, self._cache[text]))
            else:
                texts_to_embed.append(text)
                text_indices.append(idx)

        if texts_to_embed:
            new_embeddings = self._model.encode(texts_to_embed, convert_to_numpy=True).tolist()
            for text, embedding in zip(texts_to_embed, new_embeddings):
                self._cache[text] = embedding
                embeddings.append((text_indices[len([e for e in embeddings if isinstance(e, tuple)])], embedding))

        embeddings.sort(key=lambda x: x[0])
        return [emb for _, emb in embeddings]

    def clear_cache(self) -> None:
        """Clear the embedding cache."""
        self._cache.clear()
