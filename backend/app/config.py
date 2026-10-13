from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""
    DATABASE_URL: str = ""
    MODEL_PROVIDER: str = "openai"
    MODEL_NAME: str = "gpt-4o-mini"
    COLLECTION_NAME: str = "enterprise_knowledge"
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        extra="ignore",
    )

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()