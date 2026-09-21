"""Plays synthesized audio through one output stream kept open for the app's
whole lifetime.

The stream is never closed between replies on purpose: closing a PortAudio
stream on the ALSA↔PipeWire plugin while its callback is still draining
(the next reply arriving before the previous one finished) double-frees
inside `snd_pcm_close` and aborts the process. Writing blocks of samples to
a single long-lived stream never touches `snd_pcm_close` until `close()`.
"""

import threading
from collections.abc import Callable

import numpy as np
import numpy.typing as npt
import sounddevice as sd

from app.constants import PIPER_SAMPLE_RATE_HZ, PLAYBACK_BLOCK_FRAMES
from app.errors import SynthesisError

_PLAYBACK_CHANNELS = 1
_PLAYBACK_DTYPE = "float32"

StreamFactory = Callable[[], sd.OutputStream]


def _open_default_output_stream() -> sd.OutputStream:
    """Open a mono float32 output stream at the Piper sample rate."""
    stream = sd.OutputStream(
        samplerate=PIPER_SAMPLE_RATE_HZ, channels=_PLAYBACK_CHANNELS, dtype=_PLAYBACK_DTYPE
    )
    stream.start()
    return stream


class AudioPlayer:
    """Blocking playback of float32 samples; a new `play` or `stop` cuts the current one."""

    def __init__(self, open_stream: StreamFactory = _open_default_output_stream) -> None:
        self._open_stream = open_stream
        self._stream: sd.OutputStream | None = None
        self._playing = threading.Lock()
        self._interrupt = threading.Event()

    def play(self, samples: npt.NDArray[np.float32]) -> float:
        """Play `samples` to the end unless interrupted; return their full duration."""
        duration_seconds = len(samples) / PIPER_SAMPLE_RATE_HZ
        self._interrupt.set()
        with self._playing:
            self._interrupt.clear()
            try:
                self._write_blocks(self._ensure_open(), samples)
            except sd.PortAudioError as exc:
                raise SynthesisError("Failed to play back synthesized audio") from exc
        return duration_seconds

    def stop(self) -> None:
        """Cut the current playback after the block being written, if any."""
        self._interrupt.set()

    def close(self) -> None:
        """Stop playback and release the output device; only safe at shutdown."""
        self.stop()
        with self._playing:
            if self._stream is not None:
                self._stream.stop()
                self._stream.close()
                self._stream = None

    def _ensure_open(self) -> sd.OutputStream:
        """Open the output stream on first use and keep it for later replies."""
        if self._stream is None:
            self._stream = self._open_stream()
        return self._stream

    def _write_blocks(self, stream: sd.OutputStream, samples: npt.NDArray[np.float32]) -> None:
        """Write `samples` block by block, checking for an interrupt between blocks."""
        for start in range(0, len(samples), PLAYBACK_BLOCK_FRAMES):
            if self._interrupt.is_set():
                return
            stream.write(np.ascontiguousarray(samples[start : start + PLAYBACK_BLOCK_FRAMES]))
