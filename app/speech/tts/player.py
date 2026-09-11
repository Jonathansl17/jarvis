"""Plays back synthesized speech audio."""

import numpy as np
import numpy.typing as npt
import sounddevice as sd

from app.constants import PIPER_SAMPLE_RATE_HZ
from app.errors import SynthesisError


class AudioPlayer:
    """Plays mono float32 audio and reports how long it took, for the UI."""

    def play(self, samples: npt.NDArray[np.float32]) -> float:
        """Play `samples` to completion and return their duration in seconds."""
        duration_seconds = len(samples) / PIPER_SAMPLE_RATE_HZ
        try:
            sd.play(samples, samplerate=PIPER_SAMPLE_RATE_HZ)
            sd.wait()
        except sd.PortAudioError as exc:
            raise SynthesisError("Failed to play back synthesized audio") from exc
        return duration_seconds

    def stop(self) -> None:
        """Cut playback short, e.g. when the user starts talking over the assistant."""
        sd.stop()
