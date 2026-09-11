"""Pure: a `PenguinPose` plus an optional `Expression` -> a `PIL.Image`.

No `customtkinter`/`tkinter` import — testable and reusable without a Tk
display, per the architecture plan's dependency-direction rule.
"""

from PIL import Image, ImageDraw

from app.ui.avatar.expressions import Expression, cheeks_for
from app.ui.avatar.shapes import BELLY, BODY, FEET, HEAD, CANVAS_SIZE_PX, Ellipse, Line, Polygon, Shape
from app.ui.avatar.spec import PenguinPose


def render_pose(
    pose: PenguinPose, expression: Expression | None, size_px: tuple[int, int]
) -> Image.Image:
    """Draw one avatar frame, back-to-front per §7's z-order, and resize it."""
    canvas = Image.new("RGBA", (CANVAS_SIZE_PX, CANVAS_SIZE_PX), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    for shape in _z_order(pose, expression):
        _draw_shape(draw, shape)
    if size_px != (CANVAS_SIZE_PX, CANVAS_SIZE_PX):
        canvas = canvas.resize(size_px, Image.LANCZOS)
    return canvas


def _z_order(pose: PenguinPose, expression: Expression | None) -> tuple[Shape, ...]:
    """Assemble the frame's shapes back-to-front, applying expression overrides."""
    eyes = expression.eyes if expression is not None and expression.eyes is not None else pose.eyes
    beak = expression.beak if expression is not None and expression.beak is not None else pose.beak
    flippers = (
        expression.flippers if expression is not None and expression.flippers is not None else pose.flippers
    )
    eyebrows = expression.eyebrows if expression is not None else ()
    cheeks = cheeks_for(expression)
    glow = (pose.glow_ring,) if pose.glow_ring is not None else ()
    return glow + FEET + (BODY, HEAD, BELLY) + flippers + cheeks + eyes + eyebrows + beak + pose.extra


def _draw_shape(draw: ImageDraw.ImageDraw, shape: Shape) -> None:
    """Draw one primitive with the Pillow `ImageDraw` call it maps to."""
    if isinstance(shape, Ellipse):
        draw.ellipse(shape.box, fill=shape.fill, outline=shape.outline, width=shape.width)
    elif isinstance(shape, Polygon):
        draw.polygon(shape.points, fill=shape.fill)
    elif isinstance(shape, Line):
        draw.line(shape.points, fill=shape.fill, width=shape.width)
