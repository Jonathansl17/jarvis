"""One-off decorative shapes an emotion adds beside its face: sad's tear,
fear's sweat drop, surprise's exclamation mark, disgust's tongue, and
angry's steam puff.

These are always additive (`Expression.extra` / `PenguinPose.extra`), never
substitutes for a core face part, so they cannot be hidden by an
"override if not None" rule the way eyes/beak/flippers can. The animated
per-frame variants an idle loop steps through (steam growing, the tear or
sweat drop sliding, the tongue extending, the exclamation mark popping in)
live in `decoration_frames.py`, built from these base shapes.
"""

from app.ui.avatar.shapes import ACCENT_PRIMARY, Ellipse, Polygon, Shape

AVATAR_TEAR = "#7EC8F2"
AVATAR_SWEAT = "#8FD3F4"
AVATAR_STEAM = "#FF7A45"
AVATAR_TONGUE = "#E8607A"

# A proper teardrop — a circle with a small triangle on top — under the
# outer corner of the right eye (`eyes.RIGHT_EYE_BOX`'s x1 side, 175).
_TEAR_CIRCLE_BOX = (171, 98, 181, 108)
_TEAR_TIP = ((176, 90), (169, 99), (183, 99))
TEAR_DROP: tuple[Shape, ...] = (
    Polygon(_TEAR_TIP, fill=AVATAR_TEAR),
    Ellipse(_TEAR_CIRCLE_BOX, fill=AVATAR_TEAR),
)

SWEAT_DROP: tuple[Shape, ...] = (Polygon(((190, 44), (198, 60), (190, 71), (182, 60)), fill=AVATAR_SWEAT),)

# Kept within the canvas's y >= 0 top edge (a negative box is simply
# clipped, not drawn above the frame); drawn after the head in `renderer`'s
# face layer, so it is fine for it to touch the head's rounded top.
EXCLAMATION_MARK: tuple[Shape, ...] = (
    Polygon(((126, 0), (134, 0), (132, 16), (128, 16)), fill=ACCENT_PRIMARY),
    Ellipse((126, 19, 134, 27), fill=ACCENT_PRIMARY),
)

# The tongue's two anchor points at the mouth; its tip (third point) is
# extended further down by `decoration_frames.tongue_at`.
TONGUE_ROOT = ((121, 116), (139, 116))
TONGUE_BASE_TIP_Y = 129
TONGUE: tuple[Shape, ...] = (Polygon((*TONGUE_ROOT, (130, TONGUE_BASE_TIP_Y)), fill=AVATAR_TONGUE),)

# Angry's steam puff, drawn above the head; `decoration_frames.steam_puff_at`
# grows and lifts it further, step by step, instead of holding one shape.
# Started with enough headroom below the canvas's top edge that its full
# 24px rise stays mostly on-canvas instead of vanishing immediately.
STEAM_PUFF_BASE_BOX = (117, 14, 143, 32)
