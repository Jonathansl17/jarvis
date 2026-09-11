"""Samples the webcam on a dedicated OS thread, forever: a preview frame is
grabbed at ~15 fps, while face detection and emotion classification run far
less often, reusing their last result on the frames in between.

A dedicated `threading.Thread` (rather than a coroutine on the bridge's
event loop) isolates the ~15 fps camera grab from whisper/piper/Gemini
calls, which already share that loop's default executor.
"""

import threading
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
class CameraSample:
    """One grabbed preview frame, and the most recent detection for it."""

    frame: npt.NDArray[np.uint8]
    box: BoundingBox | None
    reading: EmotionReading


@dataclass(frozen=True)
class CameraTiming:
    """How often frames are grabbed vs. how often detection actually runs."""

    frame_interval_seconds: float
    detect_interval_seconds: float


@dataclass(frozen=True)
class CameraCallbacks:
    """Where `CameraWorker` reports samples and unrecoverable failures.

    Bundled (rather than two more constructor parameters) to keep
    `CameraWorker.__init__` within the project's 4-parameter ceiling.
    """

    on_sample: Callable[[CameraSample | None], None]
    on_error: Callable[[str], None]


@dataclass
class _DetectionCache:
    """The last known face box and reading, reused between detection ticks."""

    box: BoundingBox | None = field(default=None)
    reading: EmotionReading = field(default=None)


class CameraWorker:
    """Grabs webcam frames on a daemon thread and reports each as a sample."""

    def __init__(
        self, camera: Camera, detector: EmotionDetector, timing: CameraTiming, callbacks: CameraCallbacks
    ) -> None:
        self._camera = camera
        self._detector = detector
        self._frame_interval_seconds = timing.frame_interval_seconds
        self._ticks_per_detection = max(
            1, round(timing.detect_interval_seconds / timing.frame_interval_seconds)
        )
        self._callbacks = callbacks
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        """Spawn the daemon thread that samples the webcam forever."""
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Signal the sampling loop to stop, join it, and release the webcam."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def _run(self) -> None:
        """Grab a frame every `frame_interval_seconds`, until stopped.

        If the device never opens (or fails outright, e.g. held by another
        process), report the failure via `on_error` and stop — retrying
        forever would just spam a device that will not recover on its own.
        """
        cache = _DetectionCache()
        try:
            tick = 0
            while not self._stop_event.wait(self._frame_interval_seconds):
                try:
                    frame = self._camera.grab_frame()
                except EmotionDetectionError as exc:
                    self._callbacks.on_error(str(exc))
                    return
                should_detect = tick % self._ticks_per_detection == 0
                self._callbacks.on_sample(self._build_sample(frame, cache, should_detect))
                tick += 1
        finally:
            self._camera.close()

    def _build_sample(
        self,
        frame: npt.NDArray[np.uint8] | None,
        cache: _DetectionCache,
        should_detect: bool,
    ) -> CameraSample | None:
        """Return the sample for one grabbed frame, refreshing `cache` if due."""
        if frame is None:
            return None
        if should_detect:
            cache.box, cache.reading = self._detect(frame)
        return CameraSample(frame=frame, box=cache.box, reading=cache.reading)

    def _detect(
        self, frame: npt.NDArray[np.uint8]
    ) -> tuple[BoundingBox | None, EmotionReading]:
        """Classify one frame, treating a detection failure as no face found."""
        try:
            detection = self._detector.detect(frame)
        except EmotionDetectionError:
            detection = None
        if detection is None:
            return None, None
        return detection.box, (detection.emotion, detection.confidence)
