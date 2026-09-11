"""The contract for turning recorded audio into text."""

from typing import Protocol

import numpy as np
import numpy.typing as npt


class SpeechToText(Protocol):
    """Transcribes one mono, 16 kHz float32 audio clip, blocking."""

    def transcribe(self, audio: npt.NDArray[np.float32]) -> str: ...
