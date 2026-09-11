"""Process configuration, read once from the environment."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

from app.constants import MODELS_DIR_ENV_VAR

_DEFAULT_MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"
_DEFAULT_HOST = "0.0.0.0"
_DEFAULT_PORT = 8000


class Settings(BaseSettings):
    """Typed, validated startup configuration for the API process.

    `models_dir` is read from the `MODELS_DIR_ENV_VAR` environment variable;
    `host` and `port` are matched case-insensitively against environment
    variables of the same name by `pydantic-settings`, with no extra prefix.
    """

    models_dir: Path = Field(default=_DEFAULT_MODELS_DIR, validation_alias=MODELS_DIR_ENV_VAR)
    host: str = _DEFAULT_HOST
    port: int = _DEFAULT_PORT


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide `Settings` singleton."""
    return Settings()
