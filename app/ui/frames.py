"""Penguin avatar frame data, copied verbatim from the visual spec's §7
revision (see the design handoff's "Penguin avatar art" section).

Every row literal below is reproduced exactly as drawn — column alignment is
what keeps the frame from jittering between states, so nothing here is
"improved" or reformatted. `_frame` only assembles the per-state rows with
the ones every frame shares (head/torso borders, feet, resting flippers),
matching the spec's own "static rows shared by every single frame" split.
Emotion overlays live in `ui/emotion_overlay.py`.
"""

from enum import StrEnum


class AvatarState(StrEnum):
    """The behavioral states the avatar's body/border render, per §7."""

    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"


_MARGIN_BLANK = "                        "
_HEAD_TOP = "      ╭─────────╮       "
_HEAD_INTERIOR_BLANK = "      │         │       "
_HEAD_BOTTOM = "      ╰─────────╯       "
_TORSO_TOP = "      ╭─────────╮       "
_TORSO_FLIPPERS_REST = "      │ ◖     ◗ │       "
_TORSO_BOTTOM = "      ╰─────────╯       "
_FEET = "         ╨    ╨         "


def _frame(margin: str, eyes: str, beak: str, row7: str = _MARGIN_BLANK) -> tuple[str, ...]:
    """Assemble one 12-row frame from its varying rows and the shared ones."""
    return (
        margin,
        _HEAD_TOP,
        eyes,
        _HEAD_INTERIOR_BLANK,
        _HEAD_INTERIOR_BLANK,
        beak,
        _HEAD_BOTTOM,
        row7,
        _TORSO_TOP,
        _TORSO_FLIPPERS_REST,
        _TORSO_BOTTOM,
        _FEET,
    )


_EYES_OPEN = "      │ ◠     ◠ │       "
_EYES_NARROW = "      │ ─     ─ │       "
_EYES_ALERT = "      │ ◉     ◉ │       "
_BEAK_CLOSED = "      │    ▽    │       "
_BEAK_LISTENING = "      │    ○    │       "
_BEAK_HALF_OPEN = "      │   ◁ ▷   │       "
_BEAK_OPEN = "      │  ◁   ▷  │       "

# Idle — 2-frame loop (2000ms each), blink is Frame B held 150ms.
_IDLE_FRAME_OPEN = _frame(_MARGIN_BLANK, _EYES_OPEN, _BEAK_CLOSED)
_IDLE_FRAME_BLINK = _frame(_MARGIN_BLANK, _EYES_NARROW, _BEAK_CLOSED)

# Listening — 2-frame flipper-ear pulse loop (400ms/frame); row 7 is the
# reserved slot for the live mic waveform (§7.2), left blank.
_LISTENING_FRAME_REST = _frame("    ╲              ╱    ", _EYES_ALERT, _BEAK_LISTENING)
_LISTENING_FRAME_OUT = _frame("   ╲                ╱   ", _EYES_ALERT, _BEAK_LISTENING)

# Thinking — 4-frame orbiting-dots loop, 300ms/frame; only row 7 changes.
_THINKING_DOT_ROWS = (
    "          ●○○○          ",
    "          ○●○○          ",
    "          ○○●○          ",
    "          ○○○●          ",
)
_THINKING_FRAMES = tuple(
    _frame(_MARGIN_BLANK, _EYES_NARROW, _BEAK_CLOSED, row7=dots) for dots in _THINKING_DOT_ROWS
)

# Speaking — 3 beak-width frames, minimum 120ms/frame.
_SPEAKING_CLOSED = _frame(_MARGIN_BLANK, _EYES_OPEN, _BEAK_CLOSED)
_SPEAKING_HALF_OPEN = _frame(_MARGIN_BLANK, _EYES_OPEN, _BEAK_HALF_OPEN)
_SPEAKING_OPEN = _frame(_MARGIN_BLANK, _EYES_ALERT, _BEAK_OPEN)

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
        "\n".join(_LISTENING_FRAME_OUT),
    ],
}

# Waveform ramp, 0 (silence) to 7 (peak), driven by normalized mic RMS (§7.2).
WAVEFORM_GLYPHS = (" ", "▁", "▂", "▃", "▄", "▅", "▆", "▇", "█")
