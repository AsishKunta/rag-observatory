"""Tests for chunking and hybrid retrieval."""

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import fresh_embedding_service

fresh_embedding_service()  # makes the app import below safe without the real model

from app.config.settings import settings  # noqa: E402
from app.services.retrieval_service import RetrievalService, split_into_chunks  # noqa: E402

JAVA_DOC = (
    "Java manages memory with garbage collection. "
    "The garbage collection process reclaims memory from unreachable objects."
)
PYTHON_DOC = "A Python list is an ordered, mutable collection of items."


class SplitIntoChunksTests(unittest.TestCase):
    def test_short_text_is_a_single_chunk(self):
        self.assertEqual(split_into_chunks("short text"), ["short text"])

    def test_long_text_is_split_into_bounded_chunks(self):
        text = " ".join(f"Sentence number {i} is here." for i in range(80))
        chunks = split_into_chunks(text, size=400, overlap=100)

        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 400 for chunk in chunks))

    def test_chunks_cover_the_whole_text(self):
        text = " ".join(f"Sentence number {i} is here." for i in range(80))
        chunks = split_into_chunks(text, size=400, overlap=100)

        self.assertTrue(text.startswith(chunks[0]))
        self.assertTrue(text.endswith(chunks[-1]))


class HybridRetrievalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        upload_dir = Path(self.tmp.name)
        self.processed = upload_dir / "processed"
        self.processed.mkdir()
        patcher = mock.patch.object(settings, "upload_dir", upload_dir)
        patcher.start()
        self.addCleanup(patcher.stop)

        fresh_embedding_service()
        self.service = RetrievalService()

    def add_document(self, name: str, text: str) -> None:
        (self.processed / name).write_text(text, encoding="utf-8")

    def test_returns_most_relevant_document_first(self):
        self.add_document("java.txt", JAVA_DOC)
        self.add_document("python.txt", PYTHON_DOC)

        result = self.service.search_semantic("How does Java garbage collection manage memory?")

        self.assertEqual(result["matches"][0]["source"], "java.txt")
        self.assertGreater(result["confidence"], 0.5)

    def test_semantic_scoring_survives_a_newly_uploaded_document(self):
        # Regression: after the first query cached the Java chunks, uploading a
        # second document produced a mixed cached/new embedding batch, which
        # crashed the cache and silently fell back to keyword-only scoring.
        self.add_document("java.txt", JAVA_DOC)
        self.service.search_semantic("java memory")

        self.add_document("python.txt", PYTHON_DOC)
        with self.assertNoLogs("app.services.retrieval_service", level="ERROR"):
            result = self.service.search_semantic("python list")

        self.assertEqual(result["matches"][0]["source"], "python.txt")

    def test_no_documents_returns_empty_result(self):
        result = self.service.search_semantic("anything at all")

        self.assertEqual(result["matches"], [])
        self.assertEqual(result["confidence"], 0.0)


if __name__ == "__main__":
    unittest.main()
