"""Captures microphone audio while toggled on, through one input stream kept
open for the app's whole lifetime.

The stream is started and stopped per recording but never closed between
them: closing a PortAudio stream on the ALSA↔PipeWire plugin can double-free
inside `snd_pcm_close` and abort the process (see `tts/player.py`). Only
`close()`, at shutdown, releases the device.
"""

import threading
from collections.abc import Callable

import numpy as np
import numpy.typing as npt
import sounddevice as sd

from app.constants import STT_SAMPLE_RATE_HZ
from app.errors import SpeechRecognitionError

_RECORDING_CHANNELS = 1
_RECORDING_DTYPE = "float32"

AudioCallback = Callable[..., None]
StreamFactory = Callable[[AudioCallback], sd.InputStream]


def _open_default_input_stream(callback: AudioCallback) -> sd.InputStream:
    """Open (without starting) a mono float32 input stream at the whisper rate."""
    return sd.InputStream(
        samplerate=STT_SAMPLE_RATE_HZ, channels=_RECORDING_CHANNELS, dtype=_RECORDING_DTYPE, callback=callback
    )


class AudioRecorder:
    """Records mono microphone audio at `STT_SAMPLE_RATE_HZ` between calls."""

    def __init__(self, open_stream: StreamFactory = _open_default_input_stream) -> None:
        self._open_stream = open_stream
        self._chunks: list[npt.NDArray[np.float32]] = []
        self._stream: sd.InputStream | None = None
        self._recording = threading.Event()

    def start(self) -> None:
        """Begin recording from the default input device."""
        if self._recording.is_set():
            raise SpeechRecognitionError("Recording already in progress")

        self._chunks = []
        try:
            stream = self._ensure_open()
            self._recording.set()
            stream.start()
        except sd.PortAudioError as exc:
            self._recording.clear()
            raise SpeechRecognitionError("Failed to open the microphone") from exc

    def stop(self) -> npt.NDArray[np.float32]:
        """Stop recording and return the captured audio as mono float32 samples."""
        if not self._recording.is_set() or self._stream is None:
            raise SpeechRecognitionError("No recording in progress")

        try:
            self._stream.stop()
        except sd.PortAudioError as exc:
            raise SpeechRecognitionError("Failed to stop the microphone") from exc
        finally:
            self._recording.clear()

        if not self._chunks:
            return np.empty(0, dtype=np.float32)
        return np.concatenate(self._chunks).reshape(-1)

    def close(self) -> None:
        """Release the input device; only safe at shutdown."""
        self._recording.clear()
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None

    def _ensure_open(self) -> sd.InputStream:
        """Open the input stream on first use and keep it for later recordings."""
        if self._stream is None:
            self._stream = self._open_stream(self._on_audio_block)
        return self._stream

    def _on_audio_block(
        self,
        block: npt.NDArray[np.float32],
        frame_count: int,
        time_info: object,
        status: sd.CallbackFlags,
    ) -> None:
        """Append one captured audio block, called on PortAudio's own thread."""
        if self._recording.is_set():
            self._chunks.append(block.copy())
