"""Idle state frames: an 8-frame breathing loop (neutral's own animation),
plus a blink and a flipper wave the animator splices in on independent
timers regardless of which loop is active, plus a one-shot hop played after
a happy/surprise reply, plus a 3-frame transition played whenever the
displayed emotion changes so the switch reads as a reaction rather than a
cut (see `animator.AvatarAnimator.set_emotion`).

Every other emotion's own idle loop (happy's bounce, sad's sway, angry's
steam, surprise's pop, fear's jitter, disgust's turn) lives in `loops/`,
one module per emotion, and is appended to this module's flat `IDLE_FRAMES`
tuple — see `emotion_poses.IDLE_LOOP_FOR_EMOTION` for which range of it each
emotion plays instead of breathing.

All groups live in one flat `IDLE_FRAMES` tuple, addressed by the index
constants below, so `AvatarAnimator` can jump into any of them while still
caching every frame by the same `(state, index, emotion)` key the renderer
already uses for a plain loop.
"""

from app.ui.avatar.loops import (
    ANGRY_FRAMES,
    DISGUST_FRAMES,
    FEAR_FRAMES,
    HAPPY_FRAMES,
    SAD_FRAMES,
    SURPRISE_FRAMES,
)
from app.ui.avatar.pose_shapes import FLIPPERS_WAVE_MID, FLIPPERS_WAVE_UP
from app.ui.avatar.pose_types import PenguinPose
from app.ui.avatar.shape_transforms import scaled_ellipse
from app.ui.avatar.shapes import BEAK_CLOSED, BODY, EYES_BLINK, EYES_OPEN, FLIPPERS_DEFAULT

# An 8-step, 2.4s breathing cycle that eases the torso up to 1.02x scale and
# back, rather than jumping between two sizes.
_BREATHE_FRAME_MS = 300
_BREATHE_SCALES = (1.000, 1.005, 1.010, 1.015, 1.020, 1.015, 1.010, 1.005)
IDLE_BREATHE_FRAME_COUNT = len(_BREATHE_SCALES)

_BLINK_DURATION_MS = 120
_WAVE_FRAME_MS = 220
_HOP_FRAME_MS = 150
_HOP_HEIGHT_PX = 6

# The reaction transition: body scale 1.05 -> 0.98 -> 1.0, quick enough
# (120ms/frame) to read as a beat, not a delay, before the new emotion's
# own loop takes over.
_TRANSITION_FRAME_MS = 120
_TRANSITION_SCALES = (1.05, 0.98, 1.00)

IDLE_BLINK_INDEX = IDLE_BREATHE_FRAME_COUNT
IDLE_WAVE_START_INDEX = IDLE_BLINK_INDEX + 1
IDLE_WAVE_FRAME_COUNT = 3
IDLE_HOP_START_INDEX = IDLE_WAVE_START_INDEX + IDLE_WAVE_FRAME_COUNT
IDLE_HOP_FRAME_COUNT = 2
IDLE_TRANSITION_START_INDEX = IDLE_HOP_START_INDEX + IDLE_HOP_FRAME_COUNT
IDLE_TRANSITION_FRAME_COUNT = len(_TRANSITION_SCALES)

_EMOTION_LOOPS_START_INDEX = IDLE_TRANSITION_START_INDEX + IDLE_TRANSITION_FRAME_COUNT


def _breathe_pose(scale: float) -> PenguinPose:
    body = scaled_ellipse(BODY, scale)
    return PenguinPose(_BREATHE_FRAME_MS, None, FLIPPERS_DEFAULT, EYES_OPEN, BEAK_CLOSED, body=body)


def _transition_pose(scale: float) -> PenguinPose:
    """A generic reaction-beat frame: only `body` is pre-scaled, so whatever
    expression the newly set emotion resolves to still supplies the actual
    eyes/beak/flippers/eyebrows/cheeks look."""
    body = scaled_ellipse(BODY, scale)
    return PenguinPose(_TRANSITION_FRAME_MS, None, FLIPPERS_DEFAULT, EYES_OPEN, BEAK_CLOSED, body=body)


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

_TRANSITION_FRAMES = tuple(_transition_pose(scale) for scale in _TRANSITION_SCALES)

_EMOTION_LOOPS = (HAPPY_FRAMES, SAD_FRAMES, ANGRY_FRAMES, SURPRISE_FRAMES, FEAR_FRAMES, DISGUST_FRAMES)


def _emotion_loop_start(index: int) -> int:
    """The `IDLE_FRAMES` start index of the `index`-th loop in `_EMOTION_LOOPS`."""
    return _EMOTION_LOOPS_START_INDEX + sum(len(loop) for loop in _EMOTION_LOOPS[:index])


IDLE_HAPPY_START_INDEX = _emotion_loop_start(0)
IDLE_SAD_START_INDEX = _emotion_loop_start(1)
IDLE_ANGRY_START_INDEX = _emotion_loop_start(2)
IDLE_SURPRISE_START_INDEX = _emotion_loop_start(3)
IDLE_FEAR_START_INDEX = _emotion_loop_start(4)
IDLE_DISGUST_START_INDEX = _emotion_loop_start(5)

IDLE_FRAMES: tuple[PenguinPose, ...] = (
    _BREATHE_FRAMES + _BLINK_FRAMES + _WAVE_FRAMES + _HOP_FRAMES + _TRANSITION_FRAMES + sum(_EMOTION_LOOPS, ())
)
