from __future__ import annotations
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

APP_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = APP_DIR / "storage"
REPORTS_DIR = STORAGE_DIR / "reports"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENV: str = "dev"

    # DB / Redis
    DATABASE_URL: str = ""
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery
    CELERY_BROKER_URL: str = ""
    CELERY_RESULT_BACKEND: str = ""

    # Sentry
    SENTRY_DSN_BACKEND: str | None = None
    SENTRY_ENV: str = "dev"
    SENTRY_TRACES_SAMPLE_RATE: float = 0.1

    # Front (CORS)
    CORS_ORIGINS: str = "http://localhost:5173"

    FREE_JOBS_PER_DAY: int = 5


settings = Settings()
