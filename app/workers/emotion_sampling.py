"""Samples the webcam on a fixed interval, off the event loop, forever."""

import asyncio
from collections.abc import Callable

from app.emotion.camera import Camera
from app.emotion.protocol import Emotion, EmotionDetector
from app.errors import EmotionDetectionError

EmotionReading = tuple[Emotion, float] | None


async def sample_emotion_forever(
    camera: Camera,
    detector: EmotionDetector,
    interval_seconds: float,
    on_emotion: Callable[[EmotionReading], None],
) -> None:
    """Grab and classify one frame every `interval_seconds`, reporting each result."""
    while True:
        reading = await asyncio.to_thread(_sample_once, camera, detector)
        on_emotion(reading)
        await asyncio.sleep(interval_seconds)


def _sample_once(camera: Camera, detector: EmotionDetector) -> EmotionReading:
    """Grab one frame and classify it, treating a detection failure as no reading."""
    frame = camera.grab_frame()
    if frame is None:
        return None
    try:
        return detector.detect(frame)
    except EmotionDetectionError:
        return None
