"""Applies an emotion's eye/mouth glyphs onto whatever avatar frame is active
(§7.5 of the design spec).
"""

from app.emotion.protocol import Emotion

_EYE_ROW_INDEX = 2
_MOUTH_ROW_INDEX = 5
# Both rows share one inner content width: `│ <7 chars> │`, margins included.
_CONTENT_SLOT_WIDTH = 7

_EMOTION_EYES: dict[Emotion, str] = {
    Emotion.HAPPY: "◠     ◠",
    Emotion.SAD: "◡     ◡",
    Emotion.ANGRY: "◣     ◢",
    Emotion.SURPRISE: "O     O",
    Emotion.NEUTRAL: "◠     ◠",
    Emotion.FEAR: "Ö     Ö",
    Emotion.DISGUST: "◠     ◠",
}
_EMOTION_MOUTHS: dict[Emotion, str] = {
    Emotion.HAPPY: "◡◡◡",
    Emotion.SAD: "⌢",
    Emotion.ANGRY: "▭",
    Emotion.SURPRISE: "o",
    Emotion.NEUTRAL: "▽",
    Emotion.FEAR: "﹏",
    Emotion.DISGUST: "~",
}

# Never mirror a hostile-reading expression back at the user (§7.5 policy);
# the true label still reaches the status bar separately.
MIRRORED_EMOTION: dict[Emotion, Emotion] = {
    Emotion.ANGRY: Emotion.NEUTRAL,
    Emotion.DISGUST: Emotion.NEUTRAL,
}


def apply_emotion_overlay(frame: str, emotion: Emotion) -> str:
    """Return `frame` with its eye and mouth rows swapped for `emotion`."""
    display_emotion = MIRRORED_EMOTION.get(emotion, emotion)
    lines = frame.split("\n")
    lines[_EYE_ROW_INDEX] = _overlay_row(lines[_EYE_ROW_INDEX], _EMOTION_EYES[display_emotion])
    lines[_MOUTH_ROW_INDEX] = _overlay_row(
        lines[_MOUTH_ROW_INDEX], _EMOTION_MOUTHS[display_emotion]
    )
    return "\n".join(lines)


def _overlay_row(row: str, glyph: str) -> str:
    """Replace the centered glyph slot inside one `│ ... │` row."""
    prefix, separator, suffix = row.partition("│ ")
    if not separator:
        return row
    _content, tail_separator, tail = suffix.rpartition(" │")
    if not tail_separator:
        return row
    return f"{prefix}│ {glyph.center(_CONTENT_SLOT_WIDTH)} │{tail}"
