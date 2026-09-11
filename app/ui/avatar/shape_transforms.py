"""Geometric transforms shared across pose frames: a per-axis scale about a
shape's own center (idle's breathing, an emotion's "taller"/"shrunk" body),
a whole-frame shift (the speaking-state bounce, the post-reply hop, an
emotion's body offset/jitter), and a degrees-to-px approximation for "tilt"
— all computed from a single factor/offset rather than by retyping any
shape's coordinates.

Kept out of `shapes.py` to stay within its file-size limit.
"""

import math

from app.ui.avatar.shapes import Ellipse, Line, Polygon, Shape

# Half the torso's own height, used to turn a "tilt in degrees" into an
# approximate horizontal px shift — the shape system has no per-part
# rotation primitive, so a body/head tilt or turn is approximated as a
# small translation instead of an actual rotation.
_TILT_LEVER_ARM_PX = 100


def scaled_ellipse(base: Ellipse, scale_x: float, scale_y: float | None = None) -> Ellipse:
    """Scale `base`'s box by `scale_x`/`scale_y` about its own center.

    `scale_y` defaults to `scale_x` for a uniform scale.
    """
    scale_y = scale_x if scale_y is None else scale_y
    x0, y0, x1, y1 = base.box
    center_x, center_y = (x0 + x1) / 2, (y0 + y1) / 2
    half_width, half_height = (x1 - x0) / 2 * scale_x, (y1 - y0) / 2 * scale_y
    box = (center_x - half_width, center_y - half_height, center_x + half_width, center_y + half_height)
    return Ellipse(box, fill=base.fill, outline=base.outline, width=base.width)


def tilt_to_dx(tilt_deg: float) -> int:
    """Approximate a body "tilt" of `tilt_deg` as a horizontal px shift."""
    return round(_TILT_LEVER_ARM_PX * math.tan(math.radians(tilt_deg)))


def translate_shapes(shapes: tuple[Shape, ...], dy: int, dx: int = 0) -> tuple[Shape, ...]:
    """Shift every shape in `shapes` by `(dx, dy)` (negative moves up/left)."""
    return tuple(_translate_shape(shape, dx, dy) for shape in shapes)


def _translate_shape(shape: Shape, dx: int, dy: int) -> Shape:
    """Shift one shape's geometry by `(dx, dy)`, preserving its style."""
    if isinstance(shape, Ellipse):
        x0, y0, x1, y1 = shape.box
        return Ellipse(
            (x0 + dx, y0 + dy, x1 + dx, y1 + dy), fill=shape.fill, outline=shape.outline, width=shape.width
        )
    if isinstance(shape, Polygon):
        return Polygon(tuple((x + dx, y + dy) for x, y in shape.points), fill=shape.fill)
    return Line(tuple((x + dx, y + dy) for x, y in shape.points), fill=shape.fill, width=shape.width)
