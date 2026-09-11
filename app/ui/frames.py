"""Avatar frame data, copied verbatim from the JarvisTEC visual spec (§7).

Every literal block below is reproduced exactly as drawn — column alignment
is what keeps the frame from jittering between states, so nothing here is
"improved" or reformatted. Emotion overlays live in `ui/emotion_overlay.py`.
"""

from enum import StrEnum

_ART_HEIGHT_ROWS = 12


class AvatarState(StrEnum):
    """The behavioral states the avatar's body/border render, per §7."""

    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"


def _padded(lines: tuple[str, ...]) -> list[str]:
    """Pad a literal frame block with blank lines up to the fixed art height."""
    blank_count = _ART_HEIGHT_ROWS - len(lines)
    return [*lines, *([""] * blank_count)]


# §7.1 Idle — 2-frame loop (2000ms each), blink is Frame B held 150ms.
_IDLE_FRAME_OPEN = (
    "        │",
    "   ┌────┴────┐",
    "   │ ◠     ◠ │",
    "   │         │",
    "   │    ▽    │",
    "   │  ─────  │",
    "   └─────────┘",
)
_IDLE_FRAME_BLINK = (
    "        │",
    "   ┌────┴────┐",
    "   │ ─     ─ │",
    "   │         │",
    "   │    ▽    │",
    "   │  ─────  │",
    "   └─────────┘",
)

# §7.3 Thinking — 4-frame orbiting-dots loop, 300ms/frame.
_THINKING_HEAD = (
    "        │",
    "   ┌────┴────┐",
    "   │ ─     ─ │",
    "   │         │",
    "   │    ·    │",
    "   │  ─────  │",
    "   └─────────┘",
)
_THINKING_DOT_ROWS = ("●○○○", "○●○○", "○○●○", "○○○●")

# §7.4 Speaking — 3 mouth frames, minimum 120ms/frame, border pulses 180ms.
_SPEAKING_CLOSED = (
    "        │",
    "   ┌────┴────┐",
    "   │ ◠     ◠ │",
    "   │         │",
    "   │    ▽    │",
    "   │  ─────  │",
    "   └─────────┘",
)
_SPEAKING_HALF_OPEN = (
    "        │",
    "   ┌────┴────┐",
    "   │ ◠     ◠ │",
    "   │         │",
    "   │    ▽    │",
    "   │  ⎯⎯○⎯⎯  │",
    "   └─────────┘",
)
_SPEAKING_OPEN = (
    "        │",
    "   ┌────┴────┐",
    "   │ ◉     ◉ │",
    "   │         │",
    "   │    ▽    │",
    "   │  ╰───╯  │",
    "   └─────────┘",
)

# §7.2 Listening — "ears" resting position; the pulse's outward position
# shifts each ear one column away from the antenna.
_LISTENING_EARS_REST = "    ⟨    │    ⟩"
_LISTENING_EARS_OUT = "   ⟨      │      ⟩"
_LISTENING_HEAD_BODY = (
    "   ┌────┴────┐",
    "   │ ◉     ◉ │",
    "   │         │",
    "   │    ○    │",
    "   │  ─────  │",
    "   └─────────┘",
)

AVATAR_FRAMES: dict[AvatarState, list[str]] = {
    AvatarState.IDLE: [
        "\n".join(_padded(_IDLE_FRAME_OPEN)),
        "\n".join(_padded(_IDLE_FRAME_BLINK)),
    ],
    AvatarState.THINKING: [
        "\n".join(_padded((*_THINKING_HEAD, dots))) for dots in _THINKING_DOT_ROWS
    ],
    AvatarState.SPEAKING: [
        "\n".join(_padded(_SPEAKING_CLOSED)),
        "\n".join(_padded(_SPEAKING_HALF_OPEN)),
        "\n".join(_padded(_SPEAKING_OPEN)),
    ],
    AvatarState.LISTENING: [
        "\n".join(_padded((_LISTENING_EARS_REST, *_LISTENING_HEAD_BODY))),
        "\n".join(_padded((_LISTENING_EARS_OUT, *_LISTENING_HEAD_BODY))),
    ],
}

# Waveform ramp, 0 (silence) to 7 (peak), driven by normalized mic RMS (§7.2).
WAVEFORM_GLYPHS = (" ", "▁", "▂", "▃", "▄", "▅", "▆", "▇", "█")
