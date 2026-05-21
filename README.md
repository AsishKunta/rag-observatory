# RAG Observatory

Production-inspired Retrieval Augmented Generation (RAG) system built to explore document ingestion, semantic retrieval, grounded answer generation, and AI engineering workflows.

The platform processes uploaded documents, retrieves relevant context using embeddings and hybrid retrieval strategies, and generates grounded responses using local LLM inference.

## Features

- PDF document ingestion and preprocessing
- Semantic retrieval using sentence-transformers embeddings
- Hybrid retrieval (semantic + keyword scoring)
- Grounded answer generation using Ollama
- Confidence-based retrieval metadata
- Modular service-oriented architecture
- FastAPI APIs with Swagger documentation

## Retrieval Pipeline

PDF Upload
↓
Extract Text
↓
Process Document
↓
Chunk Content
↓
Generate Embeddings
↓
Semantic Retrieval
↓
Context Assembly
↓
LLM Generation
↓
Grounded Answer
