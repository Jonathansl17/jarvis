"""Per-emotion eye shape tables, plus the alternate eyes an idle loop swaps
in on specific frames (happy's peak squint, fear's darting pupils, surprise
widening) — split out of `expression_shapes.py` to keep it within the
project's file-size limit.

Every partial lid uses `eye_shapes.lid_overlay`'s "bleed past the sclera"
technique so covering less than the full eye never leaves a visible ring of
white sclera around it — the bug that made sad's eyes render as open white
rings ("like earrings").
"""

from app.ui.avatar.eye_shapes import lid_coverage_y, lid_overlay
from app.ui.avatar.shape_transforms import scale_shapes
from app.ui.avatar.shapes import AVATAR_BELLY, AVATAR_BODY, Ellipse, Line, Shape

LEFT_EYE_BOX = (85, 65, 113, 95)
RIGHT_EYE_BOX = (147, 65, 175, 95)
PUPIL_WIDTH_PX = 14
_PUPIL_HEIGHT_PX = 14
_FACE_CENTER_PX = (130, 80)


def _sclera(box: tuple[int, int, int, int]) -> Shape:
    return Ellipse(box, fill=AVATAR_BELLY)


def _pupil(box: tuple[int, int, int, int], center_y: int, dx: int = 0) -> Shape:
    """A pupil centered horizontally in `box` (shifted by `dx` to dart), at
    a fixed `center_y` (shifted from the box's own center to look up/down).
    """
    x0, _, x1, _ = box
    center_x = (x0 + x1) / 2 + dx
    half_w, half_h = PUPIL_WIDTH_PX / 2, _PUPIL_HEIGHT_PX / 2
    box_ = (round(center_x - half_w), round(center_y - half_h), round(center_x + half_w), round(center_y + half_h))
    return Ellipse(box_, fill=AVATAR_BODY)


# Closed and smiling: an upward arc (a "^" caret) over a light eye patch so
# it reads against the head's own dark color, approximated with a 3-point
# line since `Shape` has no arc/pieslice primitive.
HAPPY_EYES = (
    Ellipse((84, 68, 114, 92), fill=AVATAR_BELLY),
    Line(((87, 88), (99, 76), (111, 88)), fill=AVATAR_BODY, width=4),
    Ellipse((146, 68, 176, 92), fill=AVATAR_BELLY),
    Line(((149, 88), (161, 76), (173, 88)), fill=AVATAR_BODY, width=4),
)
# The idle bounce's peak: an extra lid shaves more of the white patch off,
# reading as a tighter squint than the resting smile.
_HAPPY_SQUINT_BOTTOM_Y = 82
HAPPY_EYES_SQUINT = HAPPY_EYES + (
    lid_overlay((84, 68, 114, 92), _HAPPY_SQUINT_BOTTOM_Y, _HAPPY_SQUINT_BOTTOM_Y),
    lid_overlay((146, 68, 176, 92), _HAPPY_SQUINT_BOTTOM_Y, _HAPPY_SQUINT_BOTTOM_Y),
)

# Round eyes, pupils looking down, each lid a chord over the top 45% with a
# flat bottom edge tilted outward-down (outer corner droops lower).
_SAD_LID_COVERAGE = 0.45
_SAD_LID_TILT_PX = 3
_SAD_PUPIL_CENTER_Y = 87


def _sad_lid(box: tuple[int, int, int, int], outer_is_left: bool) -> Shape:
    base_y = lid_coverage_y(box, _SAD_LID_COVERAGE)
    outer_y, inner_y = base_y + _SAD_LID_TILT_PX, base_y - _SAD_LID_TILT_PX
    left_y, right_y = (outer_y, inner_y) if outer_is_left else (inner_y, outer_y)
    return lid_overlay(box, left_y, right_y)


SAD_EYES = (
    _sclera(LEFT_EYE_BOX),
    _pupil(LEFT_EYE_BOX, _SAD_PUPIL_CENTER_Y),
    _sclera(RIGHT_EYE_BOX),
    _pupil(RIGHT_EYE_BOX, _SAD_PUPIL_CENTER_Y),
    _sad_lid(LEFT_EYE_BOX, outer_is_left=True),
    _sad_lid(RIGHT_EYE_BOX, outer_is_left=False),
)

# Full round eyes with a lid over the top 40%, flat and tilted inward (the
# inner corner droops lower than the outer one, a glare rather than sad's
# outward droop) — the same safe "bleed past the sclera" lid as sad/fear.
_ANGRY_LID_COVERAGE = 0.40
_ANGRY_LID_TILT_PX = 4


def _angry_lid(box: tuple[int, int, int, int], inner_is_left: bool) -> Shape:
    base_y = lid_coverage_y(box, _ANGRY_LID_COVERAGE)
    inner_y, outer_y = base_y + _ANGRY_LID_TILT_PX, base_y - _ANGRY_LID_TILT_PX
    left_y, right_y = (inner_y, outer_y) if inner_is_left else (outer_y, inner_y)
    return lid_overlay(box, left_y, right_y)


ANGRY_EYES = (
    _sclera(LEFT_EYE_BOX),
    _pupil(LEFT_EYE_BOX, 80),
    _sclera(RIGHT_EYE_BOX),
    _pupil(RIGHT_EYE_BOX, 80),
    _angry_lid(LEFT_EYE_BOX, inner_is_left=False),
    _angry_lid(RIGHT_EYE_BOX, inner_is_left=True),
)

SURPRISE_EYES = (
    Ellipse((82, 63, 116, 97), fill=AVATAR_BELLY),
    Ellipse((95, 76, 103, 84), fill=AVATAR_BODY),
    Ellipse((144, 63, 178, 97), fill=AVATAR_BELLY),
    Ellipse((157, 76, 165, 84), fill=AVATAR_BODY),
)
# Widened further about the face's center, for the idle pop's first beat.
SURPRISE_EYES_WIDE = scale_shapes(SURPRISE_EYES, 1.15, _FACE_CENTER_PX)

# Worried: shallow, level lids (not tilted — "worried", not "sad") over
# centered pupils; the idle loop darts the pupils a full pupil-width to
# either side on top of this resting look.
_FEAR_LID_COVERAGE = 0.22
_FEAR_PUPIL_CENTER_Y = 80


def _fear_lid(box: tuple[int, int, int, int]) -> Shape:
    y = lid_coverage_y(box, _FEAR_LID_COVERAGE)
    return lid_overlay(box, y, y)


def _fear_eyes(pupil_dx: int) -> tuple[Shape, ...]:
    return (
        _sclera(LEFT_EYE_BOX),
        _pupil(LEFT_EYE_BOX, _FEAR_PUPIL_CENTER_Y, pupil_dx),
        _fear_lid(LEFT_EYE_BOX),
        _sclera(RIGHT_EYE_BOX),
        _pupil(RIGHT_EYE_BOX, _FEAR_PUPIL_CENTER_Y, pupil_dx),
        _fear_lid(RIGHT_EYE_BOX),
    )


FEAR_EYES = _fear_eyes(0)
FEAR_EYES_LOOK_LEFT = _fear_eyes(-PUPIL_WIDTH_PX)
FEAR_EYES_LOOK_RIGHT = _fear_eyes(PUPIL_WIDTH_PX)

# One eye open, the other squinted almost shut by a heavy lid — the same
# safe "bleed past the sclera" lid as sad/fear, just covering far more of
# the eye, plus a thin lash line along its exposed sliver for definition.
_DISGUST_SQUINT_COVERAGE = 0.70
_DISGUST_SQUINT_BOTTOM_Y = lid_coverage_y(RIGHT_EYE_BOX, _DISGUST_SQUINT_COVERAGE)
DISGUST_EYES = (
    _sclera(LEFT_EYE_BOX),
    _pupil(LEFT_EYE_BOX, 80),
    _sclera(RIGHT_EYE_BOX),
    lid_overlay(RIGHT_EYE_BOX, _DISGUST_SQUINT_BOTTOM_Y, _DISGUST_SQUINT_BOTTOM_Y),
    Line(((149, _DISGUST_SQUINT_BOTTOM_Y), (173, _DISGUST_SQUINT_BOTTOM_Y)), fill=AVATAR_BODY, width=3),
)
