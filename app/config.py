"""Process configuration, read once from the environment or `app/.env`."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.constants import API_BASE_URL_ENV_VAR, DEFAULT_API_BASE_URL, GEMINI_API_KEY_ENV_VAR

_ENV_FILE_PATH = Path(__file__).resolve().parent / ".env"


class Settings(BaseSettings):
    """Typed, validated startup configuration for the TUI process.

    `gemini_api_key` is optional: without it the app falls back to the
    keyword-rule parser only. `api_base_url` points at the REST API in `api/`.
    """

    model_config = SettingsConfigDict(env_file=_ENV_FILE_PATH, extra="ignore")

    gemini_api_key: str | None = Field(default=None, validation_alias=GEMINI_API_KEY_ENV_VAR)
    api_base_url: str = Field(default=DEFAULT_API_BASE_URL, validation_alias=API_BASE_URL_ENV_VAR)


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide `Settings` singleton."""
    return Settings()
