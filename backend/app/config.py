import os
import sys
from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


class EnvironmentType(str, Enum):
    """Environment classification for Trade OS deployment."""
    demo = "demo"
    development = "development"
    staging = "staging"
    production = "production"


class Settings(BaseSettings):
    # --- Environment ---
    ENVIRONMENT: EnvironmentType = EnvironmentType.development

    # --- Database ---
    DATABASE_URL: str = "postgresql+psycopg://tradeos:tradeos_secret_password@localhost:5433/trade_os"

    # --- Authentication ---
    # API key for service-to-service / development access.
    # In production, this MUST be set via env var or secrets manager.
    API_KEY: str = "tradeos_pilot_secret_key_2026"

    # --- AI / External Services ---
    OPENAI_API_KEY: str = "mock_key"

    # --- CORS ---
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"

    # --- Server ---
    PORT: int = 8000

    # --- Application metadata ---
    APP_VERSION: str = "2.0.0"

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def is_demo(self) -> bool:
        return self.ENVIRONMENT == EnvironmentType.demo

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == EnvironmentType.production

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT in (EnvironmentType.development, EnvironmentType.demo)

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()


def validate_production_config():
    """Fail-fast: crash on startup if critical production secrets are missing.

    This prevents deploying with default/empty credentials.
    Only enforced in staging and production environments.
    """
    if settings.ENVIRONMENT in (EnvironmentType.staging, EnvironmentType.production):
        errors = []
        if not settings.API_KEY:
            errors.append("API_KEY must be set in staging/production")
        if "localhost" in settings.DATABASE_URL or "tradeos_secret_password" in settings.DATABASE_URL:
            errors.append("DATABASE_URL appears to use development defaults in staging/production")
        if errors:
            for err in errors:
                print(f"[FATAL CONFIG ERROR] {err}", file=sys.stderr)
            sys.exit(1)


# Run validation on import (startup)
validate_production_config()
