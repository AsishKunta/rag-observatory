# RAG Observatory — Engineering Knowledge Assistant

A portfolio-grade starter architecture for an AI application that ingests engineering documents, supports technical question answering, and returns grounded sources.

## Project Structure

- `backend/`
  - `app/` - Python FastAPI backend package
  - `api/` - HTTP endpoints for health, uploads, and question answering
  - `services/` - business logic for document ingestion, retrieval, and citation
  - `models/` - request and response schemas for API contracts
  - `config/` - environment and application settings
- `frontend/` - placeholder for future React UI
- `docs/` - architecture and design notes
- `tests/` - automated tests and validation

## Features

- Health check endpoint for service readiness
- PDF upload endpoint with local storage
- Question answering endpoint with structured answer/source response
- Modular backend architecture prepared for extraction, chunking, embeddings, and retrieval

## Getting Started

1. Create and activate a Python virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Run the FastAPI backend:

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

4. Verify the health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"healthy"}
```

## API Endpoints

- `GET /health` — service health check
- `POST /upload` — upload a PDF engineering document
- `POST /ask` — ask a technical question and receive an answer with sources

## Notes

- Backend is implemented with FastAPI and designed to be extendable.
- Frontend is prepared as a placeholder for a future React application.
- This starter avoids external AI provider dependencies and production infrastructure.
