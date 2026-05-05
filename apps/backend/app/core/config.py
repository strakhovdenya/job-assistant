from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "job-assistant-backend"
    api_v1_prefix: str = "/api/v1"

    database_url: str = "postgresql+psycopg://job_assistant:job_assistant@postgres:5432/job_assistant"

    ai_enabled: bool = True
    ai_provider: str = "fake"
    ai_base_url: str | None = None
    ai_api_key: str | None = None
    ai_model: str = "fake-model"
    ai_timeout_seconds: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()