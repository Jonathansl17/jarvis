"""Per-emotion eyebrow line pairs (or a single line for disgust), split out
of `expression_shapes.py` since eyebrows are a distinct face part with their
own per-emotion geometry table.

Each eyebrow gets a light patch drawn behind it first, since it would
otherwise be an `AVATAR_BODY`-colored line drawn directly on the
`AVATAR_BODY`-colored head, and disappear.
"""

from app.ui.avatar.shapes import AVATAR_BELLY, AVATAR_BODY, Ellipse, Line, Shape

_WIDTH_PX = 4
_WIDTH_THICK_PX = 6
_PATCH_MARGIN_PX = 4


def _brow(points: tuple[tuple[int, int], ...], width: int) -> tuple[Shape, Shape]:
    """One eyebrow: a light patch behind an `AVATAR_BODY` line."""
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    x0, x1 = min(xs) - _PATCH_MARGIN_PX, max(xs) + _PATCH_MARGIN_PX
    y0, y1 = min(ys) - _PATCH_MARGIN_PX, max(ys) + _PATCH_MARGIN_PX
    patch = Ellipse((x0, y0, x1, y1), fill=AVATAR_BELLY)
    return (patch, Line(points, fill=AVATAR_BODY, width=width))


def _pair(left: tuple[tuple[int, int], ...], right: tuple[tuple[int, int], ...], width: int) -> tuple[Shape, ...]:
    """Build a symmetric pair of eyebrows at `width` px."""
    return _brow(left, width) + _brow(right, width)


def _single(points: tuple[tuple[int, int], ...], width: int) -> tuple[Shape, ...]:
    """Build one eyebrow (disgust only raises one side)."""
    return _brow(points, width)


# Angled outward and down, per the sad row of the expression table.
SAD_EYEBROWS = _pair(((85, 57), (113, 51)), ((147, 51), (175, 57)), _WIDTH_PX)

# Thick and slanted inward (inner corner lower than outer), per the angry row.
ANGRY_EYEBROWS = _pair(((85, 60), (113, 48)), ((147, 48), (175, 60)), _WIDTH_THICK_PX)

# Raised high and flat, per the surprise row.
SURPRISE_EYEBROWS = _pair(((85, 42), (113, 42)), ((147, 42), (175, 42)), _WIDTH_PX)

# Raised, with the inner corners higher than the outer ones, per the fear row.
FEAR_EYEBROWS = _pair(((85, 57), (113, 43)), ((147, 43), (175, 57)), _WIDTH_PX)

# Left eyebrow only, raised toward the inner corner, per the disgust row.
DISGUST_EYEBROWS = _single(((85, 58), (113, 44)), _WIDTH_PX)
