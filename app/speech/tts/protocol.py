"""The contract for turning text into speech audio."""

from typing import Protocol

import numpy as np
import numpy.typing as npt


class TextToSpeech(Protocol):
    """Synthesizes one Spanish utterance into mono float32 audio, blocking."""

    def synthesize(self, text: str) -> npt.NDArray[np.float32]: ...
