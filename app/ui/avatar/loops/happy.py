"""Happy's own idle loop: the existing bounce, plus a flipper wave on every
other bounce cycle, cheeks that swell at the top of each bounce, and eyes
that squint more at the peak — 8 frames, two 4-frame bounce cycles.
"""

from app.ui.avatar.eyes import HAPPY_EYES_SQUINT
from app.ui.avatar.pose_shapes import FLIPPERS_WAVE_MID, FLIPPERS_WAVE_UP
from app.ui.avatar.pose_types import CheekPulse, PenguinPose
from app.ui.avatar.shapes import BEAK_CLOSED, EYES_OPEN, FLIPPERS_DEFAULT

_FRAME_MS = 400
_BOUNCE_HEIGHT_PX = 6
_PEAK_CHEEK_PULSE = CheekPulse(scale=1.55, opacity=255)


def _rest(flippers_override: tuple | None = None) -> PenguinPose:
    return PenguinPose(_FRAME_MS, None, FLIPPERS_DEFAULT, EYES_OPEN, BEAK_CLOSED, flippers_override=flippers_override)


def _peak(flippers_override: tuple | None = None) -> PenguinPose:
    return PenguinPose(
        _FRAME_MS,
        None,
        FLIPPERS_DEFAULT,
        EYES_OPEN,
        BEAK_CLOSED,
        vertical_offset_px=-_BOUNCE_HEIGHT_PX,
        eyes_override=HAPPY_EYES_SQUINT,
        flippers_override=flippers_override,
        cheek=_PEAK_CHEEK_PULSE,
    )


HAPPY_FRAMES: tuple[PenguinPose, ...] = (
    _rest(),
    _peak(),
    _rest(),
    _peak(),
    _rest(FLIPPERS_WAVE_MID),
    _peak(FLIPPERS_WAVE_UP),
    _rest(FLIPPERS_WAVE_MID),
    _peak(FLIPPERS_WAVE_UP),
)
