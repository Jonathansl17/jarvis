"""Idle state frames: a 6-frame breathing loop, plus a blink and a flipper
wave the animator splices in on independent timers, plus a one-shot hop
played after a happy/surprise reply, plus three emotion-driven idle loops
(happy's bounce, angry's steam puff, fear's jitter) `AvatarAnimator` cycles
through instead of breathing while that emotion is active — see
`emotion_poses.IDLE_LOOP_FOR_EMOTION`.

All groups live in one flat `IDLE_FRAMES` tuple, addressed by the index
constants below, so `AvatarAnimator` can jump into any of them while still
caching every frame by the same `(state, index, emotion)` key the renderer
already uses for a plain loop.
"""

from app.ui.avatar.decorations import STEAM_PUFF_HIGH, STEAM_PUFF_LOW
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

# Happy's idle bounce: 2 frames alternating 0/-6px, 400ms each, an 800ms
# full cycle. Angry's steam puff and fear's beak jitter alternate the same
# way, at their own cadence.
_BOUNCE_FRAME_MS = 400
_BOUNCE_HEIGHT_PX = 6
_STEAM_FRAME_MS = 400
_JITTER_FRAME_MS = 150
_JITTER_OFFSET_PX = 2

IDLE_BLINK_INDEX = IDLE_BREATHE_FRAME_COUNT
IDLE_WAVE_START_INDEX = IDLE_BLINK_INDEX + 1
IDLE_WAVE_FRAME_COUNT = 3
IDLE_HOP_START_INDEX = IDLE_WAVE_START_INDEX + IDLE_WAVE_FRAME_COUNT
IDLE_HOP_FRAME_COUNT = 2
IDLE_BOUNCE_START_INDEX = IDLE_HOP_START_INDEX + IDLE_HOP_FRAME_COUNT
IDLE_BOUNCE_FRAME_COUNT = 2
IDLE_STEAM_START_INDEX = IDLE_BOUNCE_START_INDEX + IDLE_BOUNCE_FRAME_COUNT
IDLE_STEAM_FRAME_COUNT = 2
IDLE_JITTER_START_INDEX = IDLE_STEAM_START_INDEX + IDLE_STEAM_FRAME_COUNT
IDLE_JITTER_FRAME_COUNT = 2


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

_BOUNCE_FRAMES = (
    PenguinPose(_BOUNCE_FRAME_MS, None, FLIPPERS_DEFAULT, EYES_OPEN, BEAK_CLOSED),
    PenguinPose(
        _BOUNCE_FRAME_MS, None, FLIPPERS_DEFAULT, EYES_OPEN, BEAK_CLOSED, vertical_offset_px=-_BOUNCE_HEIGHT_PX
    ),
)

_STEAM_FRAMES = (
    PenguinPose(_STEAM_FRAME_MS, None, FLIPPERS_DEFAULT, EYES_OPEN, BEAK_CLOSED, extra=STEAM_PUFF_LOW),
    PenguinPose(_STEAM_FRAME_MS, None, FLIPPERS_DEFAULT, EYES_OPEN, BEAK_CLOSED, extra=STEAM_PUFF_HIGH),
)

_JITTER_FRAMES = (
    PenguinPose(
        _JITTER_FRAME_MS, None, FLIPPERS_DEFAULT, EYES_OPEN, BEAK_CLOSED, horizontal_offset_px=-_JITTER_OFFSET_PX
    ),
    PenguinPose(
        _JITTER_FRAME_MS, None, FLIPPERS_DEFAULT, EYES_OPEN, BEAK_CLOSED, horizontal_offset_px=_JITTER_OFFSET_PX
    ),
)

IDLE_FRAMES: tuple[PenguinPose, ...] = (
    _BREATHE_FRAMES + _BLINK_FRAMES + _WAVE_FRAMES + _HOP_FRAMES + _BOUNCE_FRAMES + _STEAM_FRAMES + _JITTER_FRAMES
)
