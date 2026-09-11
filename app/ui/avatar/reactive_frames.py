"""Listening/thinking/speaking frame tables — the three states that are a
plain looping sequence (unlike idle, which splices timed events into its
loop; see `idle_frames.py`).
"""

from app.ui.avatar.pose_shapes import EYES_LOOK_UP_LEFT, EYES_LOOK_UP_RIGHT, EYES_WIDE
from app.ui.avatar.pose_types import PenguinPose
from app.ui.avatar.shapes import (
    BEAK_CLOSED,
    BEAK_HALF_OPEN,
    BEAK_OPEN,
    EYES_OPEN,
    FLIPPERS_DEFAULT,
    FLIPPERS_RAISED,
    dot_row,
    glow_ring,
)

# Glow ring alpha 40%->80%->40% over a 1.2s pulse, in 6 equal 200ms steps.
_LISTENING_FRAME_MS = 200
_LISTENING_ALPHAS = (0x66, 0x88, 0xAA, 0xCC, 0xAA, 0x88)
LISTENING_FRAMES: tuple[PenguinPose, ...] = tuple(
    PenguinPose(_LISTENING_FRAME_MS, glow_ring(alpha), FLIPPERS_RAISED, EYES_WIDE, BEAK_CLOSED)
    for alpha in _LISTENING_ALPHAS
)

# Eyes alternate up-left/up-right every 600ms (2 ticks); the 3-dot row
# cycles every 300ms (1 tick); their combined period is 1800ms = 6 ticks.
_THINKING_FRAME_MS = 300
_THINKING_EYE_BY_TICK = (
    EYES_LOOK_UP_LEFT,
    EYES_LOOK_UP_LEFT,
    EYES_LOOK_UP_RIGHT,
    EYES_LOOK_UP_RIGHT,
    EYES_LOOK_UP_LEFT,
    EYES_LOOK_UP_LEFT,
)
THINKING_FRAMES: tuple[PenguinPose, ...] = tuple(
    PenguinPose(_THINKING_FRAME_MS, None, FLIPPERS_DEFAULT, eyes, BEAK_CLOSED, extra=dot_row(tick % 3))
    for tick, eyes in enumerate(_THINKING_EYE_BY_TICK)
)

# Beak cycle closed/half/open/half at 120ms per frame, with a 3px upward
# bounce on the fully open frame only.
_SPEAKING_FRAME_MS = 120
_SPEAKING_BOUNCE_PX = -3
_SPEAKING_BEAKS = (BEAK_CLOSED, BEAK_HALF_OPEN, BEAK_OPEN, BEAK_HALF_OPEN)
SPEAKING_FRAMES: tuple[PenguinPose, ...] = tuple(
    PenguinPose(
        _SPEAKING_FRAME_MS,
        None,
        FLIPPERS_DEFAULT,
        EYES_OPEN,
        beak,
        vertical_offset_px=_SPEAKING_BOUNCE_PX if beak is BEAK_OPEN else 0,
    )
    for beak in _SPEAKING_BEAKS
)
