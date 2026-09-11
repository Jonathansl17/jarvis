"""`TextToSpeech` implementation backed by a local Piper voice."""

from pathlib import Path

import numpy as np
import numpy.typing as npt
import onnxruntime as ort
from piper import PiperVoice

from app.constants import ONNX_INTRA_OP_THREADS, PIPER_SAMPLE_RATE_HZ
from app.errors import SynthesisError

_INT16_FULL_SCALE = 32768.0


class PiperTextToSpeech:
    """Synthesizes Spanish speech locally with a cached Piper voice."""

    def __init__(self, voice_path: Path) -> None:
        try:
            self._voice = PiperVoice.load(voice_path)
            self._voice.session = _bounded_session(voice_path)
        except (OSError, ValueError) as exc:
            raise SynthesisError(f"Failed to load Piper voice at '{voice_path}'") from exc

        if self._voice.config.sample_rate != PIPER_SAMPLE_RATE_HZ:
            raise SynthesisError(
                f"Voice sample rate {self._voice.config.sample_rate} does not match "
                f"the expected {PIPER_SAMPLE_RATE_HZ} Hz"
            )

    @property
    def sample_rate(self) -> int:
        """Return the sample rate, in Hz, of the synthesized audio."""
        return self._voice.config.sample_rate

    def synthesize(self, text: str) -> npt.NDArray[np.float32]:
        """Return mono float32 samples in [-1, 1] for the given Spanish text."""
        try:
            chunks = [chunk.audio_int16_array for chunk in self._voice.synthesize(text)]
        except (RuntimeError, ValueError) as exc:
            raise SynthesisError(f"Failed to synthesize text: '{text}'") from exc

        if not chunks:
            return np.empty(0, dtype=np.float32)

        samples_int16 = np.concatenate(chunks)
        return (samples_int16.astype(np.float32) / _INT16_FULL_SCALE).clip(-1.0, 1.0)


def _bounded_session(model_path: Path) -> ort.InferenceSession:
    """Rebuild the voice's ONNX session with a bounded thread pool."""
    options = ort.SessionOptions()
    options.intra_op_num_threads = ONNX_INTRA_OP_THREADS
    return ort.InferenceSession(str(model_path), sess_options=options, providers=["CPUExecutionProvider"])
