"""Process configuration, read once from the environment."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings

_DEFAULT_MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"
_DEFAULT_HOST = "0.0.0.0"
_DEFAULT_PORT = 8000


class Settings(BaseSettings):
    """Typed, validated startup configuration for the API process.

    Field names are matched case-insensitively against environment
    variables of the same name (e.g. `MODELS_DIR`, `HOST`, `PORT`) by
    `pydantic-settings`, with no extra prefix.
    """

    models_dir: Path = _DEFAULT_MODELS_DIR
    host: str = _DEFAULT_HOST
    port: int = _DEFAULT_PORT


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide `Settings` singleton."""
    return Settings()
