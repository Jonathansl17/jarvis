"""Strips the optional wake word from the start of a user utterance."""

from app.constants import WAKE_WORDS

_WAKE_WORD_TRAILING_CHARS = ", :"


def strip_wake_word(text: str) -> str:
    """Return `text` without a leading wake word, if the utterance opens with one."""
    stripped = text.strip()
    lowered = stripped.lower()
    for wake_word in WAKE_WORDS:
        if _starts_with_wake_word(lowered, wake_word):
            return stripped[len(wake_word) :].lstrip(_WAKE_WORD_TRAILING_CHARS)
    return stripped


def _starts_with_wake_word(lowered_text: str, wake_word: str) -> bool:
    """Check `wake_word` opens `lowered_text` on a word boundary."""
    if not lowered_text.startswith(wake_word):
        return False
    remainder = lowered_text[len(wake_word) :]
    return remainder == "" or not remainder[0].isalnum()
