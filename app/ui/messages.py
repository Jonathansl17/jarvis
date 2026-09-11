"""The vocabulary of events crossing a worker thread into the UI."""

from textual.message import Message

from app.dialogue.reply import AssistantReply
from app.workers.emotion_sampling import EmotionSample


class TranscriptReady(Message):
    """A voice recording finished transcribing into text."""

    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text


class AssistantReplied(Message):
    """The orchestrator produced a reply for the last user turn."""

    def __init__(self, reply: AssistantReply) -> None:
        super().__init__()
        self.reply = reply


class AssistantSpeakingStarted(Message):
    """Text-to-speech playback started."""


class AssistantSpeakingEnded(Message):
    """Text-to-speech playback finished."""


class EmotionUpdated(Message):
    """A new webcam sample is available, or the camera yielded nothing."""

    def __init__(self, sample: EmotionSample | None) -> None:
        super().__init__()
        self.sample = sample


class ErrorOccurred(Message):
    """A background operation failed; `detail` is shown as a SYS log line."""

    def __init__(self, detail: str) -> None:
        super().__init__()
        self.detail = detail
