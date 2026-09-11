"""Applies an emotion's eye/beak glyphs onto whatever avatar frame is active,
by column slice, matching the fixed slots `ui/frames.py` reserves for them
(§7.5 of the design spec).
"""

from app.emotion.protocol import Emotion

_EYE_ROW_INDEX = 2
_BEAK_ROW_INDEX = 3
_EYE_COL_START = 9
_EYE_COL_END = 15
_BEAK_COL_START = 10
_BEAK_COL_END = 14
_BEAK_SLOT_WIDTH = _BEAK_COL_END - _BEAK_COL_START
_TEAR_COL_INDEX = 8
_TEAR_GLYPH = ","

_EMOTION_EYES: dict[Emotion, str] = {
    Emotion.HAPPY: "◠    ◠",
    Emotion.SAD: "◡    ◡",
    Emotion.ANGRY: "◣    ◢",
    Emotion.SURPRISE: "○    ○",
    Emotion.NEUTRAL: "●    ●",
    Emotion.FEAR: "◉    ◉",
    Emotion.DISGUST: "◠    ◠",
}
_EMOTION_BEAKS: dict[Emotion, str] = {
    Emotion.HAPPY: "◡◡",
    Emotion.SAD: "⌢⌢",
    Emotion.ANGRY: "▬▬",
    Emotion.SURPRISE: "◯ ",
    Emotion.NEUTRAL: "▼▼",
    Emotion.FEAR: "﹏ ",
    Emotion.DISGUST: "~~",
}

# Never mirror a hostile-reading expression back at the user (§7.5 policy);
# the true label still reaches the status bar separately.
MIRRORED_EMOTION: dict[Emotion, Emotion] = {
    Emotion.ANGRY: Emotion.NEUTRAL,
    Emotion.DISGUST: Emotion.NEUTRAL,
}


def apply_emotion_overlay(frame: str, emotion: Emotion) -> str:
    """Return `frame` with its eye and beak slots swapped for `emotion`."""
    display_emotion = MIRRORED_EMOTION.get(emotion, emotion)
    lines = frame.split("\n")
    lines[_EYE_ROW_INDEX] = _replace_columns(
        lines[_EYE_ROW_INDEX], _EYE_COL_START, _EYE_COL_END, _EMOTION_EYES[display_emotion]
    )
    lines[_BEAK_ROW_INDEX] = _beak_row(lines[_BEAK_ROW_INDEX], display_emotion)
    return "\n".join(lines)


def _beak_row(row: str, display_emotion: Emotion) -> str:
    """Build the beak row for `display_emotion`, with the sad tear if due."""
    beak = _EMOTION_BEAKS[display_emotion].center(_BEAK_SLOT_WIDTH)
    row = _replace_columns(row, _BEAK_COL_START, _BEAK_COL_END, beak)
    if display_emotion is Emotion.SAD:
        row = _replace_columns(row, _TEAR_COL_INDEX, _TEAR_COL_INDEX + 1, _TEAR_GLYPH)
    return row


def _replace_columns(row: str, start: int, end: int, glyph: str) -> str:
    """Return `row` with the character span `[start, end)` replaced by `glyph`."""
    return row[:start] + glyph + row[end:]
