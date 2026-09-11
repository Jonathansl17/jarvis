"""Per-emotion eyebrow line pairs (or a single line for disgust), split out
of `expression_shapes.py` since eyebrows are a distinct face part with their
own per-emotion geometry table.

Every eyebrow is a plain thin stroke, no patch behind it — an earlier
patch-behind-line technique (a light ellipse sized to the line's own
bounding box) rendered as an oversized slab that read as a second pair of
eyes; a thin stroke reads fine against the dark head on its own.
"""

from app.ui.avatar.shapes import Line, Shape

_WIDTH_THIN_PX = 4
AVATAR_EYEBROW_LIGHT = "#AEB6C2"
AVATAR_EYEBROW_DARK = "#4A5568"


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

# Thin, light grey, raised high in a shallow arc (a 3-point line, like
# happy's smile caret) — not the old flat patch-backed slab, which read as
# a second pair of eyes above the real ones.
SURPRISE_EYEBROWS = _thin_pair(
    ((84, 40), (99, 30), (114, 40)), ((146, 40), (161, 30), (176, 40)), AVATAR_EYEBROW_LIGHT
)

# Thin and worried: raised, with the inner corners higher than the outer
# ones, per the fear row.
FEAR_EYEBROWS = _thin_pair(((85, 57), (113, 43)), ((147, 43), (175, 57)), AVATAR_EYEBROW_LIGHT)

# Left eyebrow only, raised toward the inner corner, per the disgust row.
DISGUST_EYEBROWS = _thin_single(((85, 58), (113, 44)), AVATAR_EYEBROW_LIGHT)
# The idle loop's frame 3: raised a further 8px.
DISGUST_EYEBROWS_RAISED = _thin_single(((85, 50), (113, 36)), AVATAR_EYEBROW_LIGHT)
