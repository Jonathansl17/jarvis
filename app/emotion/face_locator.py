"""Finds the largest face in a frame using a Haar cascade."""

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
import numpy.typing as npt

from app.constants import FACE_CASCADE_MIN_NEIGHBORS, FACE_CASCADE_SCALE_FACTOR
from app.errors import EmotionDetectionError


@dataclass(frozen=True)
class BoundingBox:
    """A face's location within a frame, in pixels."""

    x: int
    y: int
    width: int
    height: int


class FaceLocator:
    """Locates the largest face in a frame, if any."""

    def __init__(self, cascade_path: Path) -> None:
        self._cascade = cv2.CascadeClassifier(str(cascade_path))
        if self._cascade.empty():
            raise EmotionDetectionError(f"Failed to load face cascade at '{cascade_path}'")

    def locate(self, frame: npt.NDArray[np.uint8]) -> BoundingBox | None:
        """Return the largest detected face's bounding box, or `None`."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self._cascade.detectMultiScale(
            gray, FACE_CASCADE_SCALE_FACTOR, FACE_CASCADE_MIN_NEIGHBORS
        )
        if len(faces) == 0:
            return None

        largest = max(faces, key=lambda face: face[2] * face[3])
        x, y, width, height = largest
        return BoundingBox(x=int(x), y=int(y), width=int(width), height=int(height))
