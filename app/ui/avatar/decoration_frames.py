"""Per-frame variants of `decorations.py`'s base shapes, for the amount an
idle loop's decoration has grown, slid, or extended on a given frame —
angry's rising steam, sad's sliding tear, fear's sliding sweat drop,
disgust's extending tongue, and surprise's popping-in exclamation mark.
"""

from app.ui.avatar.decorations import (
    AVATAR_STEAM,
    AVATAR_TONGUE,
    EXCLAMATION_MARK,
    STEAM_PUFF_BASE_BOX,
    SWEAT_DROP,
    TEAR_DROP,
    TONGUE_BASE_TIP_Y,
    TONGUE_ROOT,
)
from app.ui.avatar.shape_transforms import scale_shapes, translate_shapes
from app.ui.avatar.shapes import ACCENT_PRIMARY, Ellipse, Polygon, Shape

_STEAM_GROWTH_PER_STEP = 6
_STEAM_RISE_PER_STEP_PX = 8
_STEAM_OPACITY_BY_STEP = ("88", "AA", "CC", "EE")
_EXCLAMATION_ANCHOR_PX = (130, 13)


def steam_puff_at(step: int) -> tuple[Shape, ...]:
    """Angry's steam puff at growth `step` (0-3): wider, taller, and lifted
    further above the head each step, restarting after step 3."""
    x0, y0, x1, y1 = STEAM_PUFF_BASE_BOX
    grow = step * _STEAM_GROWTH_PER_STEP
    box = (x0 - grow, y0, x1 + grow, y1 - grow // 2)
    puff = Ellipse(box, fill=f"{AVATAR_STEAM}{_STEAM_OPACITY_BY_STEP[step]}")
    return translate_shapes((puff,), dy=-step * _STEAM_RISE_PER_STEP_PX)


def tear_drop_at(slide_px: int) -> tuple[Shape, ...]:
    """Sad's tear, `slide_px` further down the cheek than its rest position,
    restarting at the top once it reaches the loop's full travel."""
    return translate_shapes(TEAR_DROP, dy=slide_px)


def sweat_drop_at(slide_px: int) -> tuple[Shape, ...]:
    """Fear's sweat drop, `slide_px` further down than its rest position,
    reappearing at the top once it reaches the loop's full travel."""
    return translate_shapes(SWEAT_DROP, dy=slide_px)


def tongue_at(extension_px: int) -> tuple[Shape, ...]:
    """Disgust's tongue, extended `extension_px` further past its resting
    tip — the two mouth-anchor points stay fixed; only the tip moves."""
    tip = (130, TONGUE_BASE_TIP_Y + extension_px)
    return (Polygon((*TONGUE_ROOT, tip), fill=AVATAR_TONGUE),)


def exclamation_at(scale: float, opacity_hex: str = "") -> tuple[Shape, ...]:
    """Surprise's exclamation mark, popping in at `scale` (< 1.0 while
    growing) and optionally faded to `opacity_hex` (e.g. "80") as it fades
    back out, scaled about its own vertical center so it grows in place."""
    marks = scale_shapes(EXCLAMATION_MARK, scale, _EXCLAMATION_ANCHOR_PX)
    if not opacity_hex:
        return marks
    return tuple(_with_fill(shape, f"{ACCENT_PRIMARY}{opacity_hex}") for shape in marks)


def _with_fill(shape: Shape, fill: str) -> Shape:
    """Return a copy of `shape` with a different `fill`, same geometry."""
    if isinstance(shape, Ellipse):
        return Ellipse(shape.box, fill=fill, outline=shape.outline, width=shape.width)
    return Polygon(shape.points, fill=fill)
