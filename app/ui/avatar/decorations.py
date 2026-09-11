"""One-off decorative shapes an emotion adds beside its face: sad's tear,
fear's sweat drop, surprise's exclamation mark, disgust's tongue, and
angry's steam puff (two variants, alternated by the idle loop; see
`idle_frames.py`).

These are always additive (`Expression.extra` / `PenguinPose.extra`), never
substitutes for a core face part, so they cannot be hidden by an
"override if not None" rule the way eyes/beak/flippers can.
"""

from app.ui.avatar.shapes import ACCENT_PRIMARY, Ellipse, Polygon, Shape

AVATAR_TEAR = "#5B8DEF"
AVATAR_SWEAT = "#8FD3F4"
AVATAR_STEAM = "#FF7A45"
AVATAR_TONGUE = "#E8607A"

TEAR_DROP: tuple[Shape, ...] = (Polygon(((161, 92), (167, 104), (161, 113), (155, 104)), fill=AVATAR_TEAR),)

SWEAT_DROP: tuple[Shape, ...] = (Polygon(((190, 44), (198, 60), (190, 71), (182, 60)), fill=AVATAR_SWEAT),)

# Kept within the canvas's y >= 0 top edge (a negative box is simply
# clipped, not drawn above the frame); drawn after the head in `renderer`'s
# face layer, so it is fine for it to touch the head's rounded top.
EXCLAMATION_MARK: tuple[Shape, ...] = (
    Polygon(((126, 0), (134, 0), (132, 16), (128, 16)), fill=ACCENT_PRIMARY),
    Ellipse((126, 19, 134, 27), fill=ACCENT_PRIMARY),
)

TONGUE: tuple[Shape, ...] = (Polygon(((121, 116), (139, 116), (130, 129)), fill=AVATAR_TONGUE),)

# Angry's steam puff, drawn above the head; the idle loop alternates between
# these two sizes every 400ms instead of holding one still shape.
STEAM_PUFF_LOW: tuple[Shape, ...] = (Ellipse((117, 0, 143, 18), fill=f"{AVATAR_STEAM}AA"),)
STEAM_PUFF_HIGH: tuple[Shape, ...] = (Ellipse((114, 0, 146, 12), fill=f"{AVATAR_STEAM}CC"),)
