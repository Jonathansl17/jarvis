"""Per-emotion whole-body pose data: the offset/scale every emotion applies
on top of its eyes/beak/eyebrow/flipper overrides, plus which idle loop
(plain breathing, or an emotion's own bounce/steam/jitter loop) drives it.

Approximation note: the shape system has no per-part rotation, so a "head
tilt" or "head turn" is approximated as a whole-avatar shift, and a "body
tilt in degrees" as a small horizontal shift via `shape_transforms.tilt_to_dx`.
"""

from dataclasses import dataclass

from app.emotion.protocol import Emotion
from app.ui.avatar.idle_frames import (
    IDLE_ANGRY_START_INDEX,
    IDLE_DISGUST_START_INDEX,
    IDLE_FEAR_START_INDEX,
    IDLE_HAPPY_START_INDEX,
    IDLE_SAD_START_INDEX,
    IDLE_SURPRISE_START_INDEX,
)
from app.ui.avatar.loops import (
    ANGRY_FRAMES,
    DISGUST_FRAMES,
    FEAR_FRAMES,
    HAPPY_FRAMES,
    SAD_FRAMES,
    SURPRISE_FRAMES,
)
from app.ui.avatar.shape_transforms import tilt_to_dx

_HAPPY_BODY_TILT_DEG = 4
_SAD_HEAD_DROOP_PX = 6
_ANGRY_LEAN_FORWARD_PX = 3
_SURPRISE_HEIGHT_SCALE = 1.03
_FEAR_SHRINK_SCALE = 0.96
_DISGUST_HEAD_TURN_PX = 8


@dataclass(frozen=True)
class BodyPose:
    """A whole-avatar offset and per-axis scale an `Expression` applies."""

    offset: tuple[int, int] = (0, 0)
    scale: tuple[float, float] = (1.0, 1.0)


BODY_POSES: dict[Emotion, BodyPose] = {
    Emotion.HAPPY: BodyPose(offset=(tilt_to_dx(_HAPPY_BODY_TILT_DEG), 0)),
    Emotion.SAD: BodyPose(offset=(0, _SAD_HEAD_DROOP_PX)),
    Emotion.ANGRY: BodyPose(offset=(0, _ANGRY_LEAN_FORWARD_PX)),
    Emotion.SURPRISE: BodyPose(scale=(1.0, _SURPRISE_HEIGHT_SCALE)),
    Emotion.FEAR: BodyPose(scale=(_FEAR_SHRINK_SCALE, _FEAR_SHRINK_SCALE)),
    Emotion.DISGUST: BodyPose(offset=(_DISGUST_HEAD_TURN_PX, 0)),
    Emotion.NEUTRAL: BodyPose(),
}


@dataclass(frozen=True)
class IdleLoop:
    """A contiguous run of `IDLE_FRAMES` an emotion's idle animation cycles."""

    start_index: int
    frame_count: int


# Every emotion but neutral gets its own idle loop; neutral is the one
# emotion absent from this table, keeping idle's plain breathing loop.
IDLE_LOOP_FOR_EMOTION: dict[Emotion, IdleLoop] = {
    Emotion.HAPPY: IdleLoop(IDLE_HAPPY_START_INDEX, len(HAPPY_FRAMES)),
    Emotion.SAD: IdleLoop(IDLE_SAD_START_INDEX, len(SAD_FRAMES)),
    Emotion.ANGRY: IdleLoop(IDLE_ANGRY_START_INDEX, len(ANGRY_FRAMES)),
    Emotion.SURPRISE: IdleLoop(IDLE_SURPRISE_START_INDEX, len(SURPRISE_FRAMES)),
    Emotion.FEAR: IdleLoop(IDLE_FEAR_START_INDEX, len(FEAR_FRAMES)),
    Emotion.DISGUST: IdleLoop(IDLE_DISGUST_START_INDEX, len(DISGUST_FRAMES)),
}
