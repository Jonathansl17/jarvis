"""Angry's own idle loop: the steam puff grows through 4 steps (rising 24px
total) then restarts — twice per loop — while the body shakes 4px
horizontally through the middle frames, the eyebrows twitch inward on the
last frame, and the cheeks pulse redder as the steam peaks — 8 frames.
"""

from app.ui.avatar.decoration_frames import steam_puff_at
from app.ui.avatar.eyebrows import ANGRY_EYEBROWS_TWITCH
from app.ui.avatar.pose_types import CheekPulse, PenguinPose
from app.ui.avatar.shapes import BEAK_CLOSED, EYES_OPEN, FLIPPERS_DEFAULT

_FRAME_MS = 350
_SHAKE_OFFSETS_PX = (0, 0, -4, 4, -4, 4, 0, 0)
_STEAM_STEP_BY_FRAME = (0, 1, 2, 3, 0, 1, 2, 3)
_STEAM_PEAK_FRAME_INDICES = frozenset({3, 7})
_TWITCH_FRAME_INDEX = 7
_PEAK_CHEEK_PULSE = CheekPulse(scale=1.1, opacity=255)


def _frame(index: int) -> PenguinPose:
    return PenguinPose(
        _FRAME_MS,
        None,
        FLIPPERS_DEFAULT,
        EYES_OPEN,
        BEAK_CLOSED,
        extra=steam_puff_at(_STEAM_STEP_BY_FRAME[index]),
        horizontal_offset_px=_SHAKE_OFFSETS_PX[index],
        eyebrows_override=ANGRY_EYEBROWS_TWITCH if index == _TWITCH_FRAME_INDEX else None,
        cheek=_PEAK_CHEEK_PULSE if index in _STEAM_PEAK_FRAME_INDICES else None,
    )


ANGRY_FRAMES: tuple[PenguinPose, ...] = tuple(_frame(index) for index in range(len(_SHAKE_OFFSETS_PX)))
