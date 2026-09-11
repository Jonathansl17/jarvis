"""Formats one detected-emotion reading into the exact text both the camera
card's emotion word and the status strip's EMO field show.

Kept as the one shared formatter so the two surfaces can never drift: a
detected emotion shows only its Spanish label. The confidence is not shown,
it is not meaningful to the user and never decides anything.
"""

from app.emotion.protocol import Emotion
from app.emotion.spanish_labels import EMOTION_LABELS_ES, NO_FACE_TEXT


def format_emotion_reading(reading: tuple[Emotion, float] | None) -> str:
    """Return "sin rostro" for no detection, else the Spanish emotion label."""
    if reading is None:
        return NO_FACE_TEXT
    emotion, _confidence = reading
    return EMOTION_LABELS_ES[emotion]
