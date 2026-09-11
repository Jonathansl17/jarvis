"""Penguin avatar frame data, drawn from the block-character penguin draft
handed off for the visual spec's revision.

Every row literal below is reproduced exactly as drawn — column alignment is
what keeps the frame from jittering between states, so nothing here is
"improved" or reformatted. `_frame` only assembles the per-state rows with
the ones every frame shares (head borders, torso fill). Emotion overlays
live in `ui/emotion_overlay.py`.
"""

from enum import StrEnum

_Body = tuple[str, str, str]  # (row 5 shoulders, row 6 flippers, row 11 feet/waveform)


class AvatarState(StrEnum):
    """The behavioral states the avatar's body/border render, per §7."""

    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"


# Rows shared, unchanged, by every state.
_ROW1 = "      ▄██████████▄      "
_ROW4 = "      ▀██▄▄▄▄▄▄██▀      "
_ROW7 = "   ▐██░░░░░░░░░░░░██▌   "
_ROW8 = "    ██░░░░░░░░░░░░██    "
_ROW9 = "     ▀██░░░░░░░░██▀     "
_ROW10 = "       ▀▀██████▀▀       "

# Row 0 (head top): plain, or with the thinking state's orbiting dots at its
# right end, always keeping the row at 24 columns.
_ROW0_BASE = "        ▄▄██████▄▄      "
_ROW0_THINKING_PREFIX = "        ▄▄██████▄▄   "

# Row 2 (eyes) and row 3 (beak): a fixed head-shape frame around a glyph
# slot, also the slots `emotion_overlay` overwrites by column slice.
_EYE_ROW_PREFIX = "     ▐██ "
_EYE_ROW_SUFFIX = " ██▌     "
_BEAK_ROW_PREFIX = "     ▐███ "
_BEAK_ROW_SUFFIX = " ███▌     "

_EYES_OPEN = "●    ●"
_EYES_BLINK = "─    ─"
_EYES_ALERT = "◉    ◉"
_EYES_THINKING = "◔    ◔"

_BEAK_CLOSED = " ▼▼ "
_BEAK_LISTENING = " ○  "
_BEAK_HALF_OPEN = " ◣◢ "
_BEAK_OPEN = "◤ ◥ "

# Body profiles (rows 5, 6, 11): resting, vs. the listening state's raised,
# spread flippers with the live mic waveform on row 11 — shifted by one
# glyph between its two frames to animate it. Row 6 is also where
# `emotion_overlay` swaps in a per-emotion flipper glyph, at columns 3-4 and
# 19-20.
_BODY_REST: _Body = (
    "    ▄██░░░░░░░░░░██▄    ",
    "   ▐██░░░░░░░░░░░░██▌   ",
    "       ▀▀▀    ▀▀▀       ",
)
_BODY_LISTENING_REST: _Body = (
    "  ▟█▄██░░░░░░░░░░██▄█▙  ",
    "  ▝▀██░░░░░░░░░░░░██▀▘  ",
    "   ▁▂▃▅▇▅▃▂▁▂▃▅▇▅▃▂▁    ",
)
_BODY_LISTENING_SHIFTED: _Body = (
    _BODY_LISTENING_REST[0],
    _BODY_LISTENING_REST[1],
    "  ▁▂▃▅▇▅▃▂▁▂▃▅▇▅▃▂▁     ",
)


def _eye_row(glyph: str) -> str:
    """Build row 2 by wrapping `glyph` in the fixed eye-slot frame."""
    return _EYE_ROW_PREFIX + glyph + _EYE_ROW_SUFFIX


def _beak_row(glyph: str) -> str:
    """Build row 3 by wrapping `glyph` in the fixed beak-slot frame."""
    return _BEAK_ROW_PREFIX + glyph + _BEAK_ROW_SUFFIX


def _frame(row0: str, eyes: str, beak: str, body: _Body) -> tuple[str, ...]:
    """Assemble one 12-row frame from its varying rows and the shared ones."""
    shoulders, flippers, feet = body
    return (
        row0,
        _ROW1,
        _eye_row(eyes),
        _beak_row(beak),
        _ROW4,
        shoulders,
        flippers,
        _ROW7,
        _ROW8,
        _ROW9,
        _ROW10,
        feet,
    )


# Idle — 2-frame loop (2000ms each), blink is Frame B held 150ms.
_IDLE_FRAME_OPEN = _frame(_ROW0_BASE, _EYES_OPEN, _BEAK_CLOSED, _BODY_REST)
_IDLE_FRAME_BLINK = _frame(_ROW0_BASE, _EYES_BLINK, _BEAK_CLOSED, _BODY_REST)

# Listening — 2-frame loop (400ms/frame).
_LISTENING_FRAME_REST = _frame(_ROW0_BASE, _EYES_ALERT, _BEAK_LISTENING, _BODY_LISTENING_REST)
_LISTENING_FRAME_SHIFTED = _frame(
    _ROW0_BASE, _EYES_ALERT, _BEAK_LISTENING, _BODY_LISTENING_SHIFTED
)

# Thinking — 4-frame orbiting-dots loop, 300ms/frame; only row 0 changes.
_THINKING_ROW0_DOTS = ("●○○", "○●○", "○○●", "○○○")
_THINKING_FRAMES = tuple(
    _frame(_ROW0_THINKING_PREFIX + dots, _EYES_THINKING, _BEAK_CLOSED, _BODY_REST)
    for dots in _THINKING_ROW0_DOTS
)

# Speaking — 3 beak-width frames, minimum 120ms/frame.
_SPEAKING_CLOSED = _frame(_ROW0_BASE, _EYES_OPEN, _BEAK_CLOSED, _BODY_REST)
_SPEAKING_HALF_OPEN = _frame(_ROW0_BASE, _EYES_OPEN, _BEAK_HALF_OPEN, _BODY_REST)
_SPEAKING_OPEN = _frame(_ROW0_BASE, _EYES_OPEN, _BEAK_OPEN, _BODY_REST)

AVATAR_FRAMES: dict[AvatarState, list[str]] = {
    AvatarState.IDLE: [
        "\n".join(_IDLE_FRAME_OPEN),
        "\n".join(_IDLE_FRAME_BLINK),
    ],
    AvatarState.THINKING: ["\n".join(frame) for frame in _THINKING_FRAMES],
    AvatarState.SPEAKING: [
        "\n".join(_SPEAKING_CLOSED),
        "\n".join(_SPEAKING_HALF_OPEN),
        "\n".join(_SPEAKING_OPEN),
    ],
    AvatarState.LISTENING: [
        "\n".join(_LISTENING_FRAME_REST),
        "\n".join(_LISTENING_FRAME_SHIFTED),
    ],
}

# Waveform ramp, 0 (silence) to 7 (peak), driven by normalized mic RMS (§7.2).
WAVEFORM_GLYPHS = (" ", "▁", "▂", "▃", "▄", "▅", "▆", "▇", "█")
