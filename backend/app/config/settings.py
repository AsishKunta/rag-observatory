"""Application configuration settings for the RAG Observatory backend."""

from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "RAG Observatory"
    environment: str = "development"
    debug: bool = True
    upload_dir: Path = Path(__file__).resolve().parents[2] / "storage" / "documents"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
