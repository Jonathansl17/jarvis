"""Holds the state of one ongoing conversation."""

from typing import Any

from app.intents.models import PendingIntent, Turn

# `emotion/protocol.py` (a later unit) will define the real `Emotion` enum;
# `Conversation` only stores whatever it is handed, so it depends on no
# concrete emotion type yet. Replace with `Emotion | None` once that module
# exists.
_EmotionValue = Any


class Conversation:
    """In-memory state for a single conversation: history, pending intent, mood."""

    def __init__(self) -> None:
        self._turns: list[Turn] = []
        self._pending: PendingIntent | None = None
        self._last_emotion: _EmotionValue | None = None

    def history(self) -> list[Turn]:
        """Return the turns exchanged so far, oldest first."""
        return list(self._turns)

    def add_turn(self, turn: Turn) -> None:
        """Append one turn to the conversation history."""
        self._turns.append(turn)

    @property
    def pending(self) -> PendingIntent | None:
        """Return the intent still waiting on missing fields, if any."""
        return self._pending

    def set_pending(self, pending: PendingIntent | None) -> None:
        """Replace the pending intent, or clear it with `None`."""
        self._pending = pending

    @property
    def last_emotion(self) -> _EmotionValue | None:
        """Return the last emotion observed for this conversation, if any."""
        return self._last_emotion

    def set_last_emotion(self, emotion: _EmotionValue | None) -> None:
        """Record the last observed emotion."""
        self._last_emotion = emotion
