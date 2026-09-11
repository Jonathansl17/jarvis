"""Geometric transforms shared across pose frames: a uniform scale about a
shape's own center (idle's breathing) and a whole-frame vertical shift (the
speaking-state bounce, the post-reply hop) — both computed from a single
factor/offset rather than by retyping any shape's coordinates.

Kept out of `shapes.py` to stay within its file-size limit.
"""

from app.ui.avatar.shapes import Ellipse, Line, Polygon, Shape


def scaled_ellipse(base: Ellipse, scale: float) -> Ellipse:
    """Scale `base`'s box by `scale`, uniformly, about its own center."""
    x0, y0, x1, y1 = base.box
    center_x, center_y = (x0 + x1) / 2, (y0 + y1) / 2
    half_width, half_height = (x1 - x0) / 2 * scale, (y1 - y0) / 2 * scale
    box = (center_x - half_width, center_y - half_height, center_x + half_width, center_y + half_height)
    return Ellipse(box, fill=base.fill, outline=base.outline, width=base.width)


def translate_shapes(shapes: tuple[Shape, ...], dy: int) -> tuple[Shape, ...]:
    """Shift every shape in `shapes` down by `dy` px (negative moves up)."""
    return tuple(_translate_shape(shape, dy) for shape in shapes)


def _translate_shape(shape: Shape, dy: int) -> Shape:
    """Shift one shape's geometry by `dy`, preserving its style attributes."""
    if isinstance(shape, Ellipse):
        x0, y0, x1, y1 = shape.box
        return Ellipse((x0, y0 + dy, x1, y1 + dy), fill=shape.fill, outline=shape.outline, width=shape.width)
    if isinstance(shape, Polygon):
        return Polygon(tuple((x, y + dy) for x, y in shape.points), fill=shape.fill)
    return Line(tuple((x, y + dy) for x, y in shape.points), fill=shape.fill, width=shape.width)
