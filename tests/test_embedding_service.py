"""Tests for EmbeddingService caching and ordering."""

import unittest

from tests.helpers import fresh_embedding_service


class EmbeddingServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = fresh_embedding_service()
        self.model = self.service._model

    def test_returns_one_embedding_per_text_in_input_order(self):
        texts = ["java memory", "python list", "pdf upload"]
        embeddings = self.service.embed(texts)
        self.assertEqual(embeddings, self.model.encode(texts).tolist())

    def test_mixed_cached_and_new_texts_keep_input_order(self):
        # Regression: this used to raise IndexError, which retrieval caught and
        # silently downgraded to keyword-only search.
        self.service.embed(["python list"])

        texts = ["java memory", "python list", "pdf upload"]
        embeddings = self.service.embed(texts)

        self.assertEqual(embeddings, self.model.encode(texts).tolist())

    def test_cached_texts_are_not_re_encoded(self):
        self.service.embed(["java memory", "python list"])
        self.model.calls.clear()

        self.service.embed(["python list", "pdf upload", "java memory"])

        self.assertEqual(self.model.calls, [["pdf upload"]])

    def test_fully_cached_batch_skips_the_model(self):
        self.service.embed(["java memory"])
        self.model.calls.clear()

        self.service.embed(["java memory", "java memory"])

        self.assertEqual(self.model.calls, [])

    def test_duplicate_new_texts_are_encoded_once(self):
        embeddings = self.service.embed(["java memory", "java memory"])

        self.assertEqual(self.model.calls, [["java memory"]])
        self.assertEqual(embeddings[0], embeddings[1])

    def test_empty_input_returns_empty_list(self):
        self.assertEqual(self.service.embed([]), [])
        self.assertEqual(self.model.calls, [])


if __name__ == "__main__":
    unittest.main()
