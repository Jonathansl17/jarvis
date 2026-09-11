"""Ensures the Spanish Piper voice exists on disk, downloading it once."""

from pathlib import Path

from piper.download_voices import download_voice

from app.constants import PIPER_MODEL_FILE_SUFFIX, PIPER_VOICE_NAME
from app.errors import SynthesisError


def ensure_voice_downloaded(cache_dir: Path) -> Path:
    """Return the path to the cached voice model, downloading it if missing."""
    model_path = cache_dir / f"{PIPER_VOICE_NAME}{PIPER_MODEL_FILE_SUFFIX}"
    if model_path.exists():
        return model_path

    cache_dir.mkdir(parents=True, exist_ok=True)
    try:
        download_voice(PIPER_VOICE_NAME, cache_dir)
    except (OSError, ValueError) as exc:
        raise SynthesisError(f"Failed to download voice '{PIPER_VOICE_NAME}'") from exc

    return model_path
