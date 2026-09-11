"""Pure: a `PenguinPose` plus an optional `Expression` -> a `PIL.Image`.

No `customtkinter`/`tkinter` import — testable and reusable without a Tk
display, per the architecture plan's dependency-direction rule.
"""

from PIL import Image, ImageDraw

from app.ui.avatar.expressions import Expression, cheeks_for
from app.ui.avatar.shape_transforms import scaled_ellipse, translate_shapes
from app.ui.avatar.shapes import AVATAR_BELLY, CANVAS_SIZE_PX, FEET, HEAD, Ellipse, Line, Polygon, Shape, belly_shape
from app.ui.avatar.spec import PenguinPose


def render_pose(
    pose: PenguinPose, expression: Expression | None, size_px: tuple[int, int]
) -> Image.Image:
    """Draw one avatar frame, back-to-front, and resize it."""
    canvas = Image.new("RGBA", (CANVAS_SIZE_PX, CANVAS_SIZE_PX), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    for shape in _z_order(pose, expression):
        _draw_shape(draw, shape)
    if size_px != (CANVAS_SIZE_PX, CANVAS_SIZE_PX):
        canvas = canvas.resize(size_px, Image.LANCZOS)
    return canvas


def _z_order(pose: PenguinPose, expression: Expression | None) -> tuple[Shape, ...]:
    """Assemble the frame's shapes back-to-front, applying expression
    overrides. The torso (feet/body/head/belly) and cheeks are always drawn
    first, then flippers, then every face part (eyes/eyebrows/beak) and
    decoration on top of it — so an open beak, a tongue, or a tear is never
    covered by the belly or cheeks underneath it.
    """
    eyes = expression.eyes if expression is not None and expression.eyes is not None else pose.eyes
    beak = expression.beak if expression is not None and expression.beak is not None else pose.beak
    flippers = (
        expression.flippers if expression is not None and expression.flippers is not None else pose.flippers
    )
    eyebrows = expression.eyebrows if expression is not None else ()
    extra = expression.extra if expression is not None else ()
    body, head, belly = _torso_for(pose, expression)
    glow = (pose.glow_ring,) if pose.glow_ring is not None else ()

    torso_layer = glow + FEET + (body, head, belly) + flippers + cheeks_for(expression)
    face_layer = eyes + eyebrows + beak + extra + pose.extra
    shapes = torso_layer + face_layer

    dx, dy = _frame_offset(pose, expression)
    if dx or dy:
        shapes = translate_shapes(shapes, dy, dx=dx)
    return shapes


def _torso_for(pose: PenguinPose, expression: Expression | None) -> tuple[Shape, Shape, Shape]:
    """Return `(body, head, belly)`, scaled by the expression's body pose."""
    belly_fill = expression.belly_fill if expression is not None else AVATAR_BELLY
    belly = belly_shape(belly_fill)
    scale = expression.body.scale if expression is not None else (1.0, 1.0)
    if scale == (1.0, 1.0):
        return pose.body, HEAD, belly
    scale_x, scale_y = scale
    return (
        scaled_ellipse(pose.body, scale_x, scale_y),
        scaled_ellipse(HEAD, scale_x, scale_y),
        scaled_ellipse(belly, scale_x, scale_y),
    )


def _frame_offset(pose: PenguinPose, expression: Expression | None) -> tuple[int, int]:
    """Combine the pose's state-driven offset with the expression's
    emotion-driven body offset into one `(dx, dy)` shift."""
    body_dx, body_dy = expression.body.offset if expression is not None else (0, 0)
    return body_dx + pose.horizontal_offset_px, body_dy + pose.vertical_offset_px


def _draw_shape(draw: ImageDraw.ImageDraw, shape: Shape) -> None:
    """Draw one primitive with the Pillow `ImageDraw` call it maps to."""
    if isinstance(shape, Ellipse):
        draw.ellipse(shape.box, fill=shape.fill, outline=shape.outline, width=shape.width)
    elif isinstance(shape, Polygon):
        draw.polygon(shape.points, fill=shape.fill)
    elif isinstance(shape, Line):
        draw.line(shape.points, fill=shape.fill, width=shape.width)
