"""Captures microphone audio while toggled on."""

import numpy as np
import numpy.typing as npt
import sounddevice as sd

from app.constants import STT_SAMPLE_RATE_HZ
from app.errors import SpeechRecognitionError

_RECORDING_CHANNELS = 1
_RECORDING_DTYPE = "float32"


class AudioRecorder:
    """Records mono microphone audio at `STT_SAMPLE_RATE_HZ` between calls."""

    def __init__(self) -> None:
        self._chunks: list[npt.NDArray[np.float32]] = []
        self._stream: sd.InputStream | None = None

    def start(self) -> None:
        """Begin recording from the default input device."""
        if self._stream is not None:
            raise SpeechRecognitionError("Recording already in progress")

        self._chunks = []
        try:
            self._stream = sd.InputStream(
                samplerate=STT_SAMPLE_RATE_HZ,
                channels=_RECORDING_CHANNELS,
                dtype=_RECORDING_DTYPE,
                callback=self._on_audio_block,
            )
            self._stream.start()
        except sd.PortAudioError as exc:
            self._stream = None
            raise SpeechRecognitionError("Failed to open the microphone") from exc

    def stop(self) -> npt.NDArray[np.float32]:
        """Stop recording and return the captured audio as mono float32 samples."""
        if self._stream is None:
            raise SpeechRecognitionError("No recording in progress")

        try:
            self._stream.stop()
            self._stream.close()
        except sd.PortAudioError as exc:
            raise SpeechRecognitionError("Failed to close the microphone") from exc
        finally:
            self._stream = None

        if not self._chunks:
            return np.empty(0, dtype=np.float32)
        return np.concatenate(self._chunks).reshape(-1)

    def _on_audio_block(
        self,
        block: npt.NDArray[np.float32],
        frame_count: int,
        time_info: object,
        status: sd.CallbackFlags,
    ) -> None:
        """Append one captured audio block, called on PortAudio's own thread."""
        self._chunks.append(block.copy())
