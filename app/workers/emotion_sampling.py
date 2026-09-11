"""Samples the webcam on a fixed interval, off the event loop, forever."""

import asyncio
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from app.emotion.camera import Camera
from app.emotion.face_locator import BoundingBox
from app.emotion.protocol import Emotion, EmotionDetector
from app.errors import EmotionDetectionError

EmotionReading = tuple[Emotion, float] | None


@dataclass(frozen=True)
class EmotionSample:
    """One sampled frame, its detected face (if any), and its reading."""

    frame: npt.NDArray[np.uint8]
    box: BoundingBox | None
    reading: EmotionReading


async def sample_emotion_forever(
    camera: Camera,
    detector: EmotionDetector,
    interval_seconds: float,
    on_sample: Callable[[EmotionSample | None], None],
) -> None:
    """Grab and classify one frame every `interval_seconds`, reporting each result.

    Always closes the camera on exit, including on cancellation, so toggling
    the camera off reliably releases the device.
    """
    try:
        while True:
            sample = await asyncio.to_thread(_sample_once, camera, detector)
            on_sample(sample)
            await asyncio.sleep(interval_seconds)
    finally:
        camera.close()


def _sample_once(camera: Camera, detector: EmotionDetector) -> EmotionSample | None:
    """Grab one frame and classify it, treating a detection failure as no face."""
    frame = camera.grab_frame()
    if frame is None:
        return None

    try:
        detection = detector.detect(frame)
    except EmotionDetectionError:
        detection = None

    if detection is None:
        return EmotionSample(frame=frame, box=None, reading=None)
    return EmotionSample(
        frame=frame, box=detection.box, reading=(detection.emotion, detection.confidence)
    )
