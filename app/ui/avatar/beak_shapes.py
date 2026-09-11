"""The round "open beak" builder and its two sizes, split out of
`shapes.py` to stay within the project's file-size limit.

An open beak is always a round "O" — an outer ellipse in the beak's own
color with a dark interior ellipse inside it — scaled up or down for how
far open it is, never the thin horizontal line an earlier two-trapezoid
shape collapsed into at a small opening.
"""

from app.ui.avatar.shapes import AVATAR_BEAK_FOOT, AVATAR_BODY, Ellipse, Shape

_BEAK_CENTER_PX = (130, 109)
_BEAK_INTERIOR_SCALE = 0.6


def beak_round_open(width_px: float, height_px: float, fill: str = AVATAR_BEAK_FOOT) -> tuple[Shape, ...]:
    """A round open beak: an orange ellipse `width_px`x`height_px` with a
    dark interior, centered on the beak position — a scaled-up/down "O",
    never a thin line, at any opening amount."""
    center_x, center_y = _BEAK_CENTER_PX
    outer = Ellipse(
        (center_x - width_px / 2, center_y - height_px / 2, center_x + width_px / 2, center_y + height_px / 2),
        fill=fill,
    )
    interior_w, interior_h = width_px * _BEAK_INTERIOR_SCALE, height_px * _BEAK_INTERIOR_SCALE
    interior = Ellipse(
        (center_x - interior_w / 2, center_y - interior_h / 2, center_x + interior_w / 2, center_y + interior_h / 2),
        fill=AVATAR_BODY,
    )
    return (outer, interior)


BEAK_HALF_OPEN = beak_round_open(14, 16)
BEAK_OPEN = beak_round_open(22, 26)
