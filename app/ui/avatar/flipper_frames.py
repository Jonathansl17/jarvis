"""Per-frame flipper overrides an idle loop swaps in on top of its
emotion's own static flipper pose — fear's trembling, disgust's one flipper
pushing further out, and surprise's flap alternating with a narrower "in"
position.

Split out from `pose_shapes.py` since those are state-driven variants and
these are emotion-idle-loop-driven ones, built from `expression_shapes.py`'s
own flipper poses rather than the plain state defaults.
"""

from app.ui.avatar.expression_shapes import FLIPPERS_COVER_FACE, FLIPPERS_DISGUST, FLIPPERS_OUT
from app.ui.avatar.shape_transforms import translate_shapes
from app.ui.avatar.shapes import FLIPPERS_DEFAULT, Shape

_FEAR_TREMBLE_PX = 6
_DISGUST_PUSH_PX = 16

FLIPPERS_TREMBLE_UP: tuple[Shape, Shape] = translate_shapes(FLIPPERS_COVER_FACE, dy=-_FEAR_TREMBLE_PX)
FLIPPERS_TREMBLE_DOWN: tuple[Shape, Shape] = translate_shapes(FLIPPERS_COVER_FACE, dy=_FEAR_TREMBLE_PX)


def disgust_push_at(push_px: int) -> tuple[Shape, Shape]:
    """One flipper (disgust's own "out" one) pushed `push_px` further out
    than `FLIPPERS_DISGUST`'s rest position; the other stays put."""
    rest, out_flipper = FLIPPERS_DISGUST
    pushed = translate_shapes((out_flipper,), dy=0, dx=push_px)[0]
    return (rest, pushed)


FLIPPERS_DISGUST_PUSH = disgust_push_at(_DISGUST_PUSH_PX)

# Surprise's flap: alternates between the fully-out pose and a narrower
# "in" position (a smaller outward translation of the same shape).
FLIPPERS_FLAP_IN: tuple[Shape, Shape] = translate_shapes(FLIPPERS_OUT, dy=0, dx=-10)
