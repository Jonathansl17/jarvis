"""Grabs frames from the webcam."""

import cv2
import numpy as np
import numpy.typing as npt

from app.constants import CAMERA_WARMUP_FRAMES
from app.errors import EmotionDetectionError


class Camera:
    """Owns one webcam capture device, opened lazily on first use."""

    def __init__(self, device_index: int) -> None:
        self._device_index = device_index
        self._capture: cv2.VideoCapture | None = None

    def grab_frame(self) -> npt.NDArray[np.uint8] | None:
        """Return one BGR frame, or `None` if the device yields nothing."""
        capture = self._ensure_open()
        read_ok, frame = capture.read()
        if not read_ok:
            return None
        return frame

    def close(self) -> None:
        """Release the underlying capture device, if it was opened."""
        if self._capture is not None:
            self._capture.release()
            self._capture = None

    def _ensure_open(self) -> cv2.VideoCapture:
        """Open the capture device on first use, raising if it never opens."""
        if self._capture is not None:
            return self._capture

        capture = cv2.VideoCapture(self._device_index)
        if not capture.isOpened():
            raise EmotionDetectionError(f"Failed to open webcam at index {self._device_index}")

        self._capture = capture
        self._warm_up(capture)
        return capture

    @staticmethod
    def _warm_up(capture: cv2.VideoCapture) -> None:
        """Discard the first frames so auto exposure settles before use."""
        for _ in range(CAMERA_WARMUP_FRAMES):
            capture.read()
