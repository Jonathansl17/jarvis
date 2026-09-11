"""The emotion vocabulary and the contract for detecting one from a frame."""

from enum import StrEnum
from typing import Protocol

import numpy as np
import numpy.typing as npt

from app.constants import EMOTION_LABELS


class Emotion(StrEnum):
    """The seven emotions the ONNX model can classify, in its softmax order."""

    ANGRY = EMOTION_LABELS[0]
    DISGUST = EMOTION_LABELS[1]
    FEAR = EMOTION_LABELS[2]
    HAPPY = EMOTION_LABELS[3]
    SAD = EMOTION_LABELS[4]
    SURPRISE = EMOTION_LABELS[5]
    NEUTRAL = EMOTION_LABELS[6]


class EmotionDetector(Protocol):
    """Classifies the dominant emotion visible in one webcam frame."""

    def detect(self, frame: npt.NDArray[np.uint8]) -> Emotion | None: ...
