"""The emotion vocabulary and the contract for detecting one from a frame."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

import numpy as np
import numpy.typing as npt

from app.constants import EMOTION_LABELS
from app.emotion.face_locator import BoundingBox


class Emotion(StrEnum):
    """The seven emotions the ONNX model can classify, in its softmax order."""

    ANGRY = EMOTION_LABELS[0]
    DISGUST = EMOTION_LABELS[1]
    FEAR = EMOTION_LABELS[2]
    HAPPY = EMOTION_LABELS[3]
    SAD = EMOTION_LABELS[4]
    SURPRISE = EMOTION_LABELS[5]
    NEUTRAL = EMOTION_LABELS[6]


@dataclass(frozen=True)
class Detection:
    """Where a face was found and what emotion it shows."""

    box: BoundingBox
    emotion: Emotion
    confidence: float


class EmotionDetector(Protocol):
    """Locates and classifies the dominant emotion visible in one webcam frame.

    `confidence` is the model's softmax score (0.0-1.0) for `emotion`.
    Returns `None` if no face was found.
    """

    def detect(self, frame: npt.NDArray[np.uint8]) -> Detection | None: ...
