"""Samples the webcam on two rhythms, off the event loop, forever: a preview
frame is grabbed often, while face detection and emotion classification run
far less often, reusing their last result in between.
"""

import asyncio
from collections.abc import Callable
from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from app.emotion.camera import Camera
from app.emotion.face_locator import BoundingBox
from app.emotion.protocol import Emotion, EmotionDetector
from app.errors import EmotionDetectionError

EmotionReading = tuple[Emotion, float] | None


@dataclass(frozen=True)
class EmotionSample:
    """One grabbed preview frame, and the most recent detection for it."""

    frame: npt.NDArray[np.uint8]
    box: BoundingBox | None
    reading: EmotionReading


@dataclass
class _DetectionCache:
    """The last known face box and reading, reused between detection ticks."""

    box: BoundingBox | None = field(default=None)
    reading: EmotionReading = field(default=None)


async def sample_emotion_forever(
    camera: Camera,
    detector: EmotionDetector,
    preview_interval_seconds: float,
    emotion_interval_seconds: float,
    on_sample: Callable[[EmotionSample | None], None],
) -> None:
    """Grab a preview frame every `preview_interval_seconds`, forever.

    Runs face detection and emotion classification only every
    `emotion_interval_seconds`, reusing the last result on the frames in
    between so the face box stays drawn on the live preview. Always closes
    the camera on exit, including on cancellation, so toggling the camera
    off reliably releases the device.
    """
    ticks_per_detection = max(1, round(emotion_interval_seconds / preview_interval_seconds))
    cache = _DetectionCache()
    try:
        tick = 0
        while True:
            frame = await asyncio.to_thread(camera.grab_frame)
            should_detect = tick % ticks_per_detection == 0
            on_sample(await _build_sample(frame, detector, cache, should_detect))
            tick += 1
            await asyncio.sleep(preview_interval_seconds)
    finally:
        camera.close()


async def _build_sample(
    frame: npt.NDArray[np.uint8] | None,
    detector: EmotionDetector,
    cache: _DetectionCache,
    should_detect: bool,
) -> EmotionSample | None:
    """Return the sample for one grabbed frame, refreshing `cache` if due."""
    if frame is None:
        return None
    if should_detect:
        cache.box, cache.reading = await asyncio.to_thread(_detect, detector, frame)
    return EmotionSample(frame=frame, box=cache.box, reading=cache.reading)


def _detect(
    detector: EmotionDetector, frame: npt.NDArray[np.uint8]
) -> tuple[BoundingBox | None, EmotionReading]:
    """Classify one frame, treating a detection failure as no face found."""
    try:
        detection = detector.detect(frame)
    except EmotionDetectionError:
        detection = None

    if detection is None:
        return None, None
    return detection.box, (detection.emotion, detection.confidence)
