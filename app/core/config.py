from __future__ import annotations

from functools import lru_cache
from pydantic import BaseSettings, Field
from typing import Optional


class Settings(BaseSettings):
    """
    Application configuration.
    Loaded from environment variables or .env file.
    """

    # =========================
    # App Info
    # =========================
    APP_NAME: str = "Genome Dashboard"
    ENV: str = Field(default="development", description="Environment name")

    # =========================
    # Server
    # =========================
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # =========================
    # Logging
    # =========================
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    # =========================
    # Performance
    # =========================
    MAX_WORKERS: int = Field(default=4, ge=1)
    ENABLE_CACHE: bool = True

    # =========================
    # Security
    # =========================# Genome Dashboard
    SECRET_KEY: Optional[str] = None

    # =========================
    # Data / Storage
    # =========================
    DATA_PATH: str = "./data"
    TEMP_PATH: str = "./tmp"

    # =========================
    # External Services (future)
    # =========================
    REDIS_URL: Optional[str] = None
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance.
    """
    return Settings()
