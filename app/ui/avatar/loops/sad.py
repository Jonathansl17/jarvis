"""Sad's own idle loop: a slow sway 6px left/right over a 2s cycle, the
tear sliding 16px down the cheek across the cycle before restarting at the
top, eyebrows lowering a touch at the sway's low point, and a small sigh
(body scale 1.0 -> 0.98 -> 1.0) once per cycle — 8 frames, 250ms each.
"""

from app.ui.avatar.decoration_frames import tear_drop_at
from app.ui.avatar.eyebrows import SAD_EYEBROWS_LOWERED
from app.ui.avatar.pose_types import PenguinPose
from app.ui.avatar.shape_transforms import scaled_ellipse
from app.ui.avatar.shapes import BEAK_CLOSED, BODY, EYES_OPEN, FLIPPERS_DEFAULT

_FRAME_MS = 250
_SWAY_OFFSETS_PX = (0, -3, -6, -3, 0, 3, 6, 3)
_TEAR_SLIDE_PX = (0, 2, 5, 7, 9, 11, 14, 16)
_SIGH_SCALES = (1.00, 1.00, 0.99, 0.98, 0.99, 1.00, 1.00, 1.00)
_LOW_POINT_FRAME_INDEX = 3


def _frame(index: int) -> PenguinPose:
    return PenguinPose(
        _FRAME_MS,
        None,
        FLIPPERS_DEFAULT,
        EYES_OPEN,
        BEAK_CLOSED,
        extra=tear_drop_at(_TEAR_SLIDE_PX[index]),
        replace_expression_extra=True,
        body=scaled_ellipse(BODY, _SIGH_SCALES[index]),
        horizontal_offset_px=_SWAY_OFFSETS_PX[index],
        eyebrows_override=SAD_EYEBROWS_LOWERED if index == _LOW_POINT_FRAME_INDEX else None,
    )


SAD_FRAMES: tuple[PenguinPose, ...] = tuple(_frame(index) for index in range(len(_SWAY_OFFSETS_PX)))
