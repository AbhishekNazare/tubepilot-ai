from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    database_url: str = "postgresql+psycopg://tubepilot:tubepilot@localhost:5432/tubepilot"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "creator_docs"
    llm_provider: str = "openai"
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4.1-mini"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()

