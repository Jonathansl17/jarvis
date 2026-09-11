"""Holds the state of one ongoing conversation."""

from app.emotion.protocol import Emotion
from app.intents.models import PendingIntent, Turn


class Conversation:
    """In-memory state for a single conversation: history, pending intent, mood."""

    def __init__(self) -> None:
        self._turns: list[Turn] = []
        self._pending: PendingIntent | None = None
        self._pending_since: int = 0
        self._last_emotion: Emotion | None = None

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
        """Replace the pending intent, or clear it with `None`.

        Starting a fresh pending intent (there was none before) marks the
        current turn count as where its flow began, so `turns_since_pending`
        never leaks turns from an earlier, unrelated request.
        """
        if pending is not None and self._pending is None:
            self._pending_since = max(len(self._turns) - 1, 0)
        self._pending = pending

    def turns_since_pending(self) -> list[Turn]:
        """Return the turns exchanged since the current pending intent began."""
        return list(self._turns[self._pending_since :])

    @property
    def last_emotion(self) -> Emotion | None:
        """Return the last emotion observed for this conversation, if any."""
        return self._last_emotion

    def set_last_emotion(self, emotion: Emotion | None) -> None:
        """Record the last observed emotion."""
        self._last_emotion = emotion
