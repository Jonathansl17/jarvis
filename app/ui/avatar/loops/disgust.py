"""Disgust's own idle loop: the head turning a further 14px away from its
resting turn and back, the tongue extending 18px and retracting, one
flipper pushing 16px further out and back, and the eyebrow raising 8px
higher on frame 3 — 8 frames.
"""

from app.ui.avatar.decoration_frames import tongue_at
from app.ui.avatar.eyebrows import DISGUST_EYEBROWS_RAISED
from app.ui.avatar.flipper_frames import disgust_push_at
from app.ui.avatar.pose_types import PenguinPose
from app.ui.avatar.shapes import BEAK_CLOSED, EYES_OPEN, FLIPPERS_DEFAULT

_FRAME_MS = 300
_EXTRA_TURN_PX = (0, 4, 8, 14, 8, 4, 0, 0)
_TONGUE_EXTENSION_PX = (0, 4, 9, 14, 18, 14, 9, 4)
_FLIPPER_PUSH_PX = (0, 4, 8, 16, 8, 4, 0, 0)
_RAISED_BROW_FRAME_INDEX = 3


def _frame(index: int) -> PenguinPose:
    return PenguinPose(
        _FRAME_MS,
        None,
        FLIPPERS_DEFAULT,
        EYES_OPEN,
        BEAK_CLOSED,
        extra=tongue_at(_TONGUE_EXTENSION_PX[index]),
        replace_expression_extra=True,
        horizontal_offset_px=_EXTRA_TURN_PX[index],
        flippers_override=disgust_push_at(_FLIPPER_PUSH_PX[index]),
        eyebrows_override=DISGUST_EYEBROWS_RAISED if index == _RAISED_BROW_FRAME_INDEX else None,
    )


DISGUST_FRAMES: tuple[PenguinPose, ...] = tuple(_frame(index) for index in range(len(_EXTRA_TURN_PX)))
