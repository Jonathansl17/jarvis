"""Per-emotion beak/flipper shape overrides, from the expression table.

Split out of `expressions.py` to stay within the project's file-size limit;
`expressions.py` only assembles these into the `EXPRESSIONS` table. Eyebrows
have their own module, `eyebrows.py`; eyes have their own, `eyes.py`, since
each is a distinct face part with its own per-emotion geometry table. This
module re-exports the eye tables so callers only need one import (matching
`expressions.py`'s existing `import ... as shapes` usage).
"""

from app.ui.avatar.eyes import (
    ANGRY_EYES,
    DISGUST_EYES,
    FEAR_EYES,
    FEAR_EYES_LOOK_LEFT,
    FEAR_EYES_LOOK_RIGHT,
    HAPPY_EYES,
    HAPPY_EYES_SQUINT,
    SAD_EYES,
    SURPRISE_EYES,
    SURPRISE_EYES_WIDE,
)
from app.ui.avatar.shapes import AVATAR_BEAK_ANGRY, AVATAR_BEAK_FOOT, AVATAR_BODY, FLIPPERS_DEFAULT, Polygon

__all__ = [
    "ANGRY_EYES",
    "DISGUST_EYES",
    "FEAR_EYES",
    "FEAR_EYES_LOOK_LEFT",
    "FEAR_EYES_LOOK_RIGHT",
    "HAPPY_EYES",
    "HAPPY_EYES_SQUINT",
    "SAD_EYES",
    "SURPRISE_EYES",
    "SURPRISE_EYES_WIDE",
]

HAPPY_BEAK = (Polygon(((112, 100), (148, 100), (130, 118)), fill=AVATAR_BEAK_FOOT),)
SAD_BEAK = (Polygon(((120, 100), (140, 100), (115, 120)), fill=AVATAR_BEAK_FOOT),)
# Flat and short, per the angry row's "beak flat".
ANGRY_BEAK = (Polygon(((114, 105), (146, 105), (140, 113), (120, 113)), fill=AVATAR_BEAK_ANGRY),)
FEAR_BEAK = (Polygon(((122, 100), (138, 100), (130, 112)), fill=AVATAR_BEAK_FOOT),)
DISGUST_BEAK = (Polygon(((110, 105), (144, 100), (128, 118)), fill=AVATAR_BEAK_FOOT),)

# Fear's beak trembles by a tiny horizontal shift each idle jitter frame
# rather than by swapping shape — see `idle_frames.py`'s jitter loop.

FLIPPERS_DROOPING = (
    Polygon(((45, 140), (18, 175), (30, 225), (55, 200)), fill=AVATAR_BODY),
    Polygon(((215, 140), (242, 175), (230, 225), (205, 200)), fill=AVATAR_BODY),
)
FLIPPERS_ANGRY = (
    Polygon(((45, 120), (18, 100), (35, 75), (55, 105)), fill=AVATAR_BODY),
    Polygon(((215, 120), (242, 100), (225, 75), (205, 105)), fill=AVATAR_BODY),
)
FLIPPERS_OUT = (
    Polygon(((45, 145), (10, 165), (25, 200), (55, 185)), fill=AVATAR_BODY),
    Polygon(((215, 145), (250, 165), (235, 200), (205, 185)), fill=AVATAR_BODY),
)
# Raised to head height, covering the sides of the face, per the fear row.
FLIPPERS_COVER_FACE = (
    Polygon(((70, 110), (35, 60), (55, 20), (85, 75)), fill=AVATAR_BODY),
    Polygon(((190, 110), (225, 60), (205, 20), (175, 75)), fill=AVATAR_BODY),
)
FLIPPERS_DISGUST = (FLIPPERS_DEFAULT[0], FLIPPERS_OUT[1])

