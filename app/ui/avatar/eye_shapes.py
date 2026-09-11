"""Shared eyelid geometry.

A lid is a head-colored polygon drawn on top of an eye's white sclera. It is
deliberately drawn bigger than the sclera on the top/left/right — bled past
it by `_LID_BLEED_PX` — so that only its flat bottom edge actually clips the
eye. A lid custom-fit tightly to the sclera's own curve left a visible ring
of white between the lid and the sclera's edge (a real bug fixed here: sad's
eyes rendered as open white rings, "like earrings"); bleeding past the
sclera on every side but the reveal edge means that never happens, because
past the sclera the same fill color already matches the head behind it.
"""

from app.ui.avatar.shapes import AVATAR_BODY, Polygon, Shape

_LID_BLEED_PX = 4


def lid_overlay(box: tuple[int, int, int, int], left_bottom_y: int, right_bottom_y: int) -> Shape:
    """A lid over the eye at `box` (x0, y0, x1, y1), covering from its top
    down to a flat bottom edge that runs from `(x0, left_bottom_y)` to
    `(x1, right_bottom_y)` — the two may differ to tilt the lid.
    """
    x0, y0, x1, _ = box
    top_y = y0 - _LID_BLEED_PX
    points = (
        (x0 - _LID_BLEED_PX, top_y),
        (x1 + _LID_BLEED_PX, top_y),
        (x1 + _LID_BLEED_PX, right_bottom_y),
        (x0 - _LID_BLEED_PX, left_bottom_y),
    )
    return Polygon(points, fill=AVATAR_BODY)


def lid_coverage_y(box: tuple[int, int, int, int], coverage: float) -> int:
    """Return the y where a lid covering the top `coverage` fraction of the
    eye at `box` would end, before either side's tilt is applied."""
    _, y0, _, y1 = box
    return round(y0 + (y1 - y0) * coverage)
