"""Retrieval service for finding relevant document chunks in extracted text files."""

import re
from pathlib import Path
from typing import Any

from app.config.settings import settings

STOP_WORDS = {"what", "is", "explain", "tell", "about", "the", "a", "an"}


def normalize_text(text: str) -> str:
    """Normalize text for matching by lowercasing and removing punctuation."""
    cleaned = re.sub(r"[^\w\s]", " ", text.lower())
    return " ".join(cleaned.split())


def text_tokens(text: str, remove_stopwords: bool = False) -> list[str]:
    """Convert normalized text into word tokens, optionally removing stop words."""
    tokens = normalize_text(text).split()
    if remove_stopwords:
        tokens = [token for token in tokens if token not in STOP_WORDS]
    return tokens


def clean_text(text: str) -> str:
    """Clean text while preserving paragraph breaks and sentence spacing."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{3,}", " ", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def format_answer(text: str) -> str:
    """Format the answer with sentence breaks and readable paragraphs."""
    text = text.strip()
    if not text:
        return text

    paragraphs = re.split(r"\n{2,}", text)
    formatted_paragraphs = []

    for paragraph in paragraphs:
        paragraph = paragraph.replace("\n", " ").strip()
        if not paragraph:
            continue
        sentences = re.split(r"(?<=[.!?])\s+", paragraph)
        formatted_paragraphs.append("\n".join(sentence.strip() for sentence in sentences if sentence.strip()))

    return "\n\n".join(formatted_paragraphs)


def split_into_chunks(text: str, size: int = 400, overlap: int = 100) -> list[str]:

    """Split text into overlapping chunks while preserving readability."""
    text = text.strip()
    if len(text) <= size:
        return [text]

    chunks: list[str] = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + size, length)
        if end < length:
            segment = text[start:end]
            sentence_break = max(
                segment.rfind('. '),
                segment.rfind('? '),
                segment.rfind('! '),
                segment.rfind('\n\n'),
            )
            if sentence_break >= size - 100:
                end = start + sentence_break + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= length:
            break
        start = max(end - overlap, end - size)

    return chunks


def truncate_answer(text: str, max_chars: int = 1200) -> str:
    """Truncate the answer at a sentence boundary while respecting a character limit."""
    if len(text) <= max_chars:
        return text

    truncated = text[:max_chars].rstrip()
    last_sentence = max(
        truncated.rfind('. '),
        truncated.rfind('? '),
        truncated.rfind('! '),
    )
    if last_sentence > max_chars - 200:
        return truncated[: last_sentence + 1].strip()

    return truncated.strip()


def score_chunk(query_tokens: list[str], chunk_tokens: list[str]) -> int:
    """Score a chunk by exact and partial query keyword overlap."""
    score = 0
    for query_token in query_tokens:
        for chunk_token in chunk_tokens:
            if query_token == chunk_token:
                score += 2
            elif query_token in chunk_token or chunk_token in query_token:
                score += 1
    return score


class RetrievalService:
    def search_documents(self, question: str) -> dict[str, list[dict[str, Any]]]:
        """Search extracted text files and return the top matching text chunks."""
        processed_dir = Path(settings.upload_dir) / "processed"
        if not processed_dir.exists():
            return {"matches": []}

        query_tokens = text_tokens(question, remove_stopwords=True)
        if not query_tokens:
            query_tokens = text_tokens(question)
        if not query_tokens:
            return {"matches": []}

        all_matches: list[dict[str, Any]] = []

        for txt_file in sorted(processed_dir.glob("*.txt")):
            raw_text = txt_file.read_text(encoding="utf-8")
            cleaned_text = clean_text(raw_text)
            chunks = split_into_chunks(cleaned_text, size=400, overlap=100)

            for chunk in chunks:
                chunk_tokens = text_tokens(chunk, remove_stopwords=True)
                score = score_chunk(query_tokens, chunk_tokens)
                all_matches.append({
                    "score": score,
                    "source": txt_file.name,
                    "content": chunk,
                })

        all_matches.sort(key=lambda item: item["score"], reverse=True)

        top_matches = [match for match in all_matches if match["score"] >= 1][:3]
        if not top_matches and all_matches:
            top_matches = all_matches[:3]

        for match in top_matches:
            answer_text = truncate_answer(match["content"], max_chars=1200)
            match["content"] = format_answer(answer_text)

        return {"matches": top_matches}
