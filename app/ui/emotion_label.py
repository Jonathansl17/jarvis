"""Formats one detected-emotion reading into the exact text both the camera
card's emotion word and the status strip's EMO field show.

Kept as the one shared formatter so the two surfaces can never drift: a
detected emotion always shows its Spanish label plus confidence percentage
(e.g. "feliz 82 %"); the confidence threshold only decides whether the
avatar mirrors the emotion (`ui.avatar.expressions`), never what either
label says.
"""

from app.emotion.protocol import Emotion
from app.emotion.spanish_labels import EMOTION_LABELS_ES, NO_FACE_TEXT

_PERCENT_MULTIPLIER = 100


def format_emotion_reading(reading: tuple[Emotion, float] | None) -> str:
    """Return "sin rostro" for no detection, else "<label> NN %"."""
    if reading is None:
        return NO_FACE_TEXT
    emotion, confidence = reading
    percentage = round(confidence * _PERCENT_MULTIPLIER)
    return f"{EMOTION_LABELS_ES[emotion]} {percentage} %"
