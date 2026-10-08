"""Shared test helpers: a deterministic stand-in for the embedding model."""

import sys
import types

import numpy as np


class FakeEmbeddingModel:
    """Deterministic stand-in for SentenceTransformer.

    Embeds text as a bag-of-words count vector over a small fixed vocabulary,
    so texts sharing words get high cosine similarity. It also records every
    batch it is asked to encode, so tests can check what reached the model.
    """

    VOCAB = ["java", "memory", "garbage", "collection", "python", "list", "pdf", "upload"]

    def __init__(self, *_args, **_kwargs):
        self.calls: list[list[str]] = []

    def encode(self, texts, convert_to_numpy=True):
        self.calls.append(list(texts))
        rows = []
        for text in texts:
            words = text.lower().split()
            row = [float(words.count(term)) for term in self.VOCAB]
            row.append(1e-3)  # keep every vector non-zero for cosine similarity
            rows.append(row)
        return np.array(rows)


def ensure_sentence_transformers_importable() -> None:
    """Register a stub module only if the real package isn't installed.

    Tests always inject FakeEmbeddingModel directly, so the real model is
    never downloaded or run; this just lets the import line succeed.
    """
    try:
        import sentence_transformers  # noqa: F401
    except ImportError:
        stub = types.ModuleType("sentence_transformers")
        stub.SentenceTransformer = FakeEmbeddingModel
        sys.modules["sentence_transformers"] = stub


def fresh_embedding_service():
    """Return a new EmbeddingService backed by a fresh FakeEmbeddingModel."""
    ensure_sentence_transformers_importable()
    from app.services.embedding_service import EmbeddingService

    EmbeddingService._instance = None
    EmbeddingService._model = FakeEmbeddingModel()
    return EmbeddingService()
