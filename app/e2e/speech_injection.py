"""A recorder that "hears" a scripted sentence instead of the room.

Wraps the real `AudioRecorder` so the microphone stream still opens, starts
and stops exactly as in normal use, but `stop()` hands back the sentence
queued with `say_next()` synthesized by Piper and resampled to whisper's
rate. Whisper then transcribes real Spanish speech, so the smoke test
covers the same path a spoken question takes, with nobody at the mic.
"""

import numpy as np
import numpy.typing as npt

from app.constants import PIPER_SAMPLE_RATE_HZ, STT_SAMPLE_RATE_HZ
from app.speech.stt.recorder import AudioRecorder, StreamFactory, open_default_input_stream
from app.speech.tts.protocol import TextToSpeech


class ScriptedSpeechRecorder(AudioRecorder):
    """Records for real, but returns synthesized speech of the queued sentence."""

    def __init__(self, tts: TextToSpeech, open_stream: StreamFactory = open_default_input_stream) -> None:
        super().__init__(open_stream)
        self._tts = tts
        self._next_text: str | None = None

    def say_next(self, text: str) -> None:
        """Queue the sentence the next `stop()` will return as audio."""
        self._next_text = text

    def stop(self) -> npt.NDArray[np.float32]:
        """Stop the real stream, then return the queued sentence as 16 kHz audio."""
        captured = super().stop()
        if self._next_text is None:
            return captured
        text, self._next_text = self._next_text, None
        return _resample(self._tts.synthesize(text), PIPER_SAMPLE_RATE_HZ, STT_SAMPLE_RATE_HZ)


def _resample(samples: npt.NDArray[np.float32], from_hz: int, to_hz: int) -> npt.NDArray[np.float32]:
    """Linear resampling; plenty for speech that only whisper will hear."""
    if len(samples) == 0:
        return samples
    target_length = int(len(samples) * to_hz / from_hz)
    positions = np.linspace(0, len(samples) - 1, target_length)
    return np.interp(positions, np.arange(len(samples)), samples).astype(np.float32)
