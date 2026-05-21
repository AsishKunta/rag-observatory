"""Application configuration settings for the RAG Observatory backend."""

from pathlib import Path


class Settings:
    app_name: str = "RAG Observatory"
    environment: str = "development"
    debug: bool = True
    upload_dir: Path = Path(__file__).resolve().parents[1] / ".." / "uploads"


settings = Settings()
