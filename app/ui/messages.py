"""The vocabulary of events crossing the bridge into the Tk main thread."""

from dataclasses import dataclass

from app.dialogue.reply import AssistantReply
from app.workers.camera_worker import CameraSample


@dataclass(frozen=True)
class TranscriptReady:
    """A voice recording finished transcribing into text."""

    text: str


@dataclass(frozen=True)
class AssistantReplied:
    """The orchestrator produced a reply for the last user turn."""

    reply: AssistantReply


@dataclass(frozen=True)
class CameraSampleReady:
    """A new webcam sample is available, or the camera yielded nothing."""

    sample: CameraSample | None


@dataclass(frozen=True)
class ErrorOccurred:
    """A background operation failed; `detail` is shown as a status-strip
    error line (never a chat line — see `dispatch_handlers.py`)."""

    detail: str


@dataclass(frozen=True)
class SpeakingFinished:
    """TTS playback finished (or failed); the avatar returns to idle.

    Added beyond the architecture plan's original four-variant vocabulary:
    `_speak()` runs on the background bridge thread, where touching a Tk
    widget directly is unsafe, so returning the avatar to idle must cross
    the same thread-safe queue as every other background result.
    """


@dataclass(frozen=True)
class CameraFailed:
    """The camera worker could not read a frame at all and stopped itself.

    Added for the same reason as `SpeakingFinished`: the worker thread must
    not call widget methods directly, and a failed camera needs a distinct
    signal from "on, but momentarily no frame" (`CameraSampleReady(None)`)
    so the toggle button and status strip can reflect the real state
    instead of silently looking merely "off".
    """

    detail: str


UiMessage = (
    TranscriptReady | AssistantReplied | CameraSampleReady | ErrorOccurred | SpeakingFinished | CameraFailed
)
