"""Rewrites a reply's phrasing to fit the user's last known emotion."""

from app.emotion.protocol import Emotion
from app.emotion.tone_table import TONE_RULES

_SENTENCE_TERMINATOR = "."


class ToneAdapter:
    """Applies a table-driven tone rewrite over an assistant reply."""

    def apply(self, text: str, emotion: Emotion | None) -> str:
        """Return `text` wrapped and, if terse, trimmed for `emotion`."""
        if emotion is None:
            return text

        rule = TONE_RULES[emotion]
        body = self._first_sentence(text) if rule.terse else text
        return f"{rule.prefix}{body}{rule.suffix}"

    def _first_sentence(self, text: str) -> str:
        """Return the first sentence of `text`, terminator included."""
        first, separator, _rest = text.partition(_SENTENCE_TERMINATOR)
        return first + separator if separator else text
