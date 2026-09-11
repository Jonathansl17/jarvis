"""`SpeechToText` implementation backed by a local faster-whisper model."""

import numpy as np
import numpy.typing as npt
from faster_whisper import WhisperModel

from app.errors import SpeechRecognitionError


class WhisperSpeechToText:
    """Transcribes audio locally with a faster-whisper model."""

    def __init__(self, model_size: str, language: str, device: str) -> None:
        self._language = language
        try:
            self._model = WhisperModel(model_size, device=device)
        except (OSError, ValueError) as exc:
            raise SpeechRecognitionError(f"Failed to load whisper model '{model_size}'") from exc

    def transcribe(self, audio: npt.NDArray[np.float32]) -> str:
        """Return the Spanish transcript of one mono, 16 kHz float32 clip."""
        try:
            segments, _info = self._model.transcribe(audio, language=self._language)
            return " ".join(segment.text.strip() for segment in segments).strip()
        except (RuntimeError, ValueError) as exc:
            raise SpeechRecognitionError("Failed to transcribe audio") from exc
