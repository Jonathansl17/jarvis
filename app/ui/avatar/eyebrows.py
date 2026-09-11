"""Per-emotion eyebrow line pairs (or a single line for disgust), split out
of `expression_shapes.py` since eyebrows are a distinct face part with their
own per-emotion geometry table.

Surprise and fear's eyebrows get a light patch drawn behind them first,
since they would otherwise be an `AVATAR_BODY`-colored line drawn directly
on the `AVATAR_BODY`-colored head, and disappear. Sad, angry, and disgust
are drawn as plain thin strokes instead — the patch technique, sized to the
line's own bounding box, rendered as an oversized slab behind their
shallower, wider-set brows; a thin stroke reads fine against the dark head
without one.
"""

from app.ui.avatar.shapes import AVATAR_BELLY, AVATAR_BODY, Ellipse, Line, Shape

_WIDTH_PX = 4
_WIDTH_THIN_PX = 4
_PATCH_MARGIN_PX = 4
AVATAR_EYEBROW_LIGHT = "#AEB6C2"
AVATAR_EYEBROW_DARK = "#4A5568"


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


def _thin_pair(
    left: tuple[tuple[int, int], ...], right: tuple[tuple[int, int], ...], color: str
) -> tuple[Shape, ...]:
    """A symmetric pair of plain thin strokes in `color`, no patch behind
    them (sad/angry's brows — see the module docstring)."""
    return (
        Line(left, fill=color, width=_WIDTH_THIN_PX),
        Line(right, fill=color, width=_WIDTH_THIN_PX),
    )


def _thin_single(points: tuple[tuple[int, int], ...], color: str) -> tuple[Shape, ...]:
    """One plain thin stroke in `color`, no patch behind it (disgust's
    single raised brow — see the module docstring)."""
    return (Line(points, fill=color, width=_WIDTH_THIN_PX),)


# Angled outward and down, per the sad row of the expression table.
SAD_EYEBROWS = _thin_pair(((85, 57), (113, 51)), ((147, 51), (175, 57)), AVATAR_EYEBROW_LIGHT)
# The idle loop's low point: eyebrows settle a touch lower still.
SAD_EYEBROWS_LOWERED = _thin_pair(((85, 60), (113, 54)), ((147, 54), (175, 60)), AVATAR_EYEBROW_LIGHT)

# Thin, dark grey, slanted inward and low over the eyes (inner corner lower
# than outer), per the angry row.
ANGRY_EYEBROWS = _thin_pair(((85, 64), (113, 52)), ((147, 52), (175, 64)), AVATAR_EYEBROW_DARK)
# The idle loop's last frame: a sharper inward twitch.
ANGRY_EYEBROWS_TWITCH = _thin_pair(((85, 66), (113, 48)), ((147, 48), (175, 66)), AVATAR_EYEBROW_DARK)

# Raised high and flat, per the surprise row.
SURPRISE_EYEBROWS = _pair(((85, 42), (113, 42)), ((147, 42), (175, 42)), _WIDTH_PX)

# Thin and worried: raised, with the inner corners higher than the outer
# ones, per the fear row.
FEAR_EYEBROWS = _thin_pair(((85, 57), (113, 43)), ((147, 43), (175, 57)), AVATAR_EYEBROW_LIGHT)

# Left eyebrow only, raised toward the inner corner, per the disgust row.
DISGUST_EYEBROWS = _thin_single(((85, 58), (113, 44)), AVATAR_EYEBROW_LIGHT)
# The idle loop's frame 3: raised a further 8px.
DISGUST_EYEBROWS_RAISED = _thin_single(((85, 50), (113, 36)), AVATAR_EYEBROW_LIGHT)
