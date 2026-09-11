"""Process configuration, read once from the environment or `app/.env`."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.constants import (
    API_BASE_URL_ENV_VAR,
    CAMERA_ENABLED_ENV_VAR,
    DEFAULT_API_BASE_URL,
    GEMINI_API_KEY_ENV_VAR,
    MODELS_DIR_ENV_VAR,
    PIPER_CACHE_DIR_ENV_VAR,
    TTS_ENABLED_ENV_VAR,
)

_ENV_FILE_PATH = Path(__file__).resolve().parent / ".env"
_DEFAULT_MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
_DEFAULT_PIPER_CACHE_DIR = Path(__file__).resolve().parent / ".cache" / "piper"
_DEFAULT_CAMERA_ENABLED = True
_DEFAULT_TTS_ENABLED = True


class Settings(BaseSettings):
    """Typed, validated startup configuration for the TUI process.

    `gemini_api_key` is optional: without it the app falls back to the
    keyword-rule parser only. `api_base_url` points at the REST API in `api/`.
    `models_dir` points at the repo-root `models/` directory shared with
    `api/`. `piper_cache_dir` is where the downloaded Spanish voice is
    cached. `camera_enabled`/`tts_enabled` let the webcam sampler and speech
    synthesis be turned off (e.g. for headless runs or automated tests).
    """

    model_config = SettingsConfigDict(env_file=_ENV_FILE_PATH, extra="ignore")

    gemini_api_key: str | None = Field(default=None, validation_alias=GEMINI_API_KEY_ENV_VAR)
    api_base_url: str = Field(default=DEFAULT_API_BASE_URL, validation_alias=API_BASE_URL_ENV_VAR)
    models_dir: Path = Field(default=_DEFAULT_MODELS_DIR, validation_alias=MODELS_DIR_ENV_VAR)
    piper_cache_dir: Path = Field(
        default=_DEFAULT_PIPER_CACHE_DIR, validation_alias=PIPER_CACHE_DIR_ENV_VAR
    )
    camera_enabled: bool = Field(
        default=_DEFAULT_CAMERA_ENABLED, validation_alias=CAMERA_ENABLED_ENV_VAR
    )
    tts_enabled: bool = Field(default=_DEFAULT_TTS_ENABLED, validation_alias=TTS_ENABLED_ENV_VAR)


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide `Settings` singleton."""
    return Settings()
