"""Idle state frames: a 6-frame breathing loop, plus a blink and a flipper
wave the animator splices in on independent timers, plus a one-shot hop
played after a happy/surprise reply.

All four groups live in one flat `IDLE_FRAMES` tuple, addressed by the
index constants below, so `AvatarAnimator` can jump into any of them while
still caching every frame by the same `(state, index, emotion)` key the
renderer already uses for a plain loop.
"""

from app.ui.avatar.pose_shapes import FLIPPERS_WAVE_MID, FLIPPERS_WAVE_UP
from app.ui.avatar.pose_types import PenguinPose
from app.ui.avatar.shape_transforms import scaled_ellipse
from app.ui.avatar.shapes import BEAK_CLOSED, BODY, EYES_BLINK, EYES_OPEN, FLIPPERS_DEFAULT

# 2.4s breathing cycle, discretized into 6 equal steps that ease the torso
# up to 1.02x scale and back, rather than jumping between two sizes.
_BREATHE_FRAME_MS = 400
_BREATHE_SCALES = (1.000, 1.007, 1.013, 1.020, 1.013, 1.007)
IDLE_BREATHE_FRAME_COUNT = len(_BREATHE_SCALES)

_BLINK_DURATION_MS = 120
_WAVE_FRAME_MS = 220
_HOP_FRAME_MS = 150
_HOP_HEIGHT_PX = 6

IDLE_BLINK_INDEX = IDLE_BREATHE_FRAME_COUNT
IDLE_WAVE_START_INDEX = IDLE_BLINK_INDEX + 1
IDLE_WAVE_FRAME_COUNT = 3
IDLE_HOP_START_INDEX = IDLE_WAVE_START_INDEX + IDLE_WAVE_FRAME_COUNT
IDLE_HOP_FRAME_COUNT = 2


def _breathe_pose(scale: float) -> PenguinPose:
    body = scaled_ellipse(BODY, scale)
    return PenguinPose(_BREATHE_FRAME_MS, None, FLIPPERS_DEFAULT, EYES_OPEN, BEAK_CLOSED, body=body)


_BREATHE_FRAMES = tuple(_breathe_pose(scale) for scale in _BREATHE_SCALES)

_BLINK_FRAMES = (PenguinPose(_BLINK_DURATION_MS, None, FLIPPERS_DEFAULT, EYES_BLINK, BEAK_CLOSED),)

_WAVE_FRAMES = (
    PenguinPose(_WAVE_FRAME_MS, None, FLIPPERS_WAVE_MID, EYES_OPEN, BEAK_CLOSED),
    PenguinPose(_WAVE_FRAME_MS, None, FLIPPERS_WAVE_UP, EYES_OPEN, BEAK_CLOSED),
    PenguinPose(_WAVE_FRAME_MS, None, FLIPPERS_DEFAULT, EYES_OPEN, BEAK_CLOSED),
)

_HOP_FRAMES = (
    PenguinPose(_HOP_FRAME_MS, None, FLIPPERS_DEFAULT, EYES_OPEN, BEAK_CLOSED, vertical_offset_px=-_HOP_HEIGHT_PX),
    PenguinPose(_HOP_FRAME_MS, None, FLIPPERS_DEFAULT, EYES_OPEN, BEAK_CLOSED),
)

IDLE_FRAMES: tuple[PenguinPose, ...] = _BREATHE_FRAMES + _BLINK_FRAMES + _WAVE_FRAMES + _HOP_FRAMES
