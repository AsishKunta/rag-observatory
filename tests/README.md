# Tests

Unit and regression tests for the RAG Observatory backend services.

Run from the repository root:

```bash
python -m pytest tests -v
# or, with no extra installs:
python -m unittest discover -s tests -t . -v
```

The tests replace the sentence-transformers model with a small deterministic
fake (`tests/helpers.py`), so they run in milliseconds, need no model download,
and do not require Ollama.

| File | Covers |
| --- | --- |
| `test_embedding_service.py` | Cache correctness: input order, mixed cached/new batches, no re-encoding, de-duplication |
| `test_document_service.py` | Upload safety: path-traversal filenames, non-PDF names and content, files staying inside the upload directory |
| `test_retrieval_service.py` | Chunking bounds and coverage; hybrid ranking; regression for semantic search after a new document upload |
