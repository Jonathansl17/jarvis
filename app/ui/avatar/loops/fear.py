"""Fear's own idle loop: a 4px jitter on both axes, the sweat drop sliding
20px down before reappearing at the top, the flippers trembling 6px up and
down in alternation, and the eyes darting a full pupil-width left/right
every 2 frames — 8 frames, fast enough (150ms each) to read as visibly
anxious rather than merely still.
"""

from app.ui.avatar.decoration_frames import sweat_drop_at
from app.ui.avatar.eyes import FEAR_EYES_LOOK_LEFT, FEAR_EYES_LOOK_RIGHT
from app.ui.avatar.flipper_frames import FLIPPERS_TREMBLE_DOWN, FLIPPERS_TREMBLE_UP
from app.ui.avatar.pose_types import PenguinPose
from app.ui.avatar.shapes import BEAK_CLOSED, EYES_OPEN, FLIPPERS_DEFAULT

_FRAME_MS = 150
_JITTER_OFFSETS_PX = ((-4, -4), (4, 4), (-4, 4), (4, -4), (-4, -4), (4, 4), (-4, 4), (4, -4))
_SWEAT_SLIDE_PX = (0, 3, 6, 9, 11, 14, 17, 20)
_DART_EYES_BY_FRAME = (
    None,
    None,
    FEAR_EYES_LOOK_LEFT,
    FEAR_EYES_LOOK_LEFT,
    None,
    None,
    FEAR_EYES_LOOK_RIGHT,
    FEAR_EYES_LOOK_RIGHT,
)


def _frame(index: int) -> PenguinPose:
    dx, dy = _JITTER_OFFSETS_PX[index]
    tremble = FLIPPERS_TREMBLE_UP if index % 2 == 0 else FLIPPERS_TREMBLE_DOWN
    return PenguinPose(
        _FRAME_MS,
        None,
        FLIPPERS_DEFAULT,
        EYES_OPEN,
        BEAK_CLOSED,
        extra=sweat_drop_at(_SWEAT_SLIDE_PX[index]),
        replace_expression_extra=True,
        horizontal_offset_px=dx,
        vertical_offset_px=dy,
        eyes_override=_DART_EYES_BY_FRAME[index],
        flippers_override=tremble,
    )


FEAR_FRAMES: tuple[PenguinPose, ...] = tuple(_frame(index) for index in range(len(_JITTER_OFFSETS_PX)))
