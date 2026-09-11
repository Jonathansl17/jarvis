"""Surprise's own idle loop: a small hop on frame 0, the exclamation mark
popping in (scale 0.6 -> 1.0 over 3 frames) then fading back out, the eyes
widening on the pop before relaxing, and the flippers flapping out and back
— 8 frames.
"""

from app.ui.avatar.decoration_frames import exclamation_at
from app.ui.avatar.eyes import SURPRISE_EYES_WIDE
from app.ui.avatar.flipper_frames import FLIPPERS_FLAP_IN
from app.ui.avatar.pose_types import PenguinPose
from app.ui.avatar.shapes import BEAK_CLOSED, EYES_OPEN, FLIPPERS_DEFAULT

_FRAME_MS = 220
_HOP_HEIGHT_PX = 6
_HOP_FRAME_INDEX = 0
_WIDE_EYES_FRAME_INDICES = frozenset({0, 1})
_FLAP_IN_FRAME_INDICES = frozenset({1, 3, 5, 7})
# scale is `None` once the mark has fully faded (empty `extra` that frame).
_EXCLAMATION_BY_FRAME: tuple[tuple[float, str] | None, ...] = (
    (0.6, ""),
    (0.8, ""),
    (1.0, ""),
    (1.0, ""),
    (1.0, "AA"),
    (1.0, "55"),
    None,
    None,
)


def _extra_for(index: int) -> tuple:
    spec = _EXCLAMATION_BY_FRAME[index]
    return exclamation_at(*spec) if spec is not None else ()


def _frame(index: int) -> PenguinPose:
    return PenguinPose(
        _FRAME_MS,
        None,
        FLIPPERS_DEFAULT,
        EYES_OPEN,
        BEAK_CLOSED,
        extra=_extra_for(index),
        replace_expression_extra=True,
        vertical_offset_px=-_HOP_HEIGHT_PX if index == _HOP_FRAME_INDEX else 0,
        eyes_override=SURPRISE_EYES_WIDE if index in _WIDE_EYES_FRAME_INDICES else None,
        flippers_override=FLIPPERS_FLAP_IN if index in _FLAP_IN_FRAME_INDICES else None,
    )


SURPRISE_FRAMES: tuple[PenguinPose, ...] = tuple(_frame(index) for index in range(len(_EXCLAMATION_BY_FRAME)))
