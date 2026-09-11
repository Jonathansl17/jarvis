"""Shape variants driven by behavioral state rather than emotion: the
listening state's wide eyes, the thinking state's look-up-left/right eyes,
and the idle wave gesture's mid-raise flipper.

Split out of `shapes.py`/`expression_shapes.py` to keep each module's line
count within the project's file-size limit; those two hold emotion-driven
overrides, these hold state-driven ones.
"""

from app.ui.avatar.expression_shapes import SURPRISE_EYES
from app.ui.avatar.shapes import AVATAR_BELLY, AVATAR_BODY, FLIPPERS_DEFAULT, FLIPPERS_RAISED, Ellipse, Polygon, Shape

# Listening's "eyes wide" reuses the surprise expression's eye shape: both
# are simply wide-open eyes, so no separate geometry is needed.
EYES_WIDE = SURPRISE_EYES

EYES_LOOK_UP_LEFT = (
    Ellipse((85, 65, 113, 95), fill=AVATAR_BELLY),
    Ellipse((88, 69, 102, 83), fill=AVATAR_BODY),
    Ellipse((147, 65, 175, 95), fill=AVATAR_BELLY),
    Ellipse((150, 69, 164, 83), fill=AVATAR_BODY),
)
EYES_LOOK_UP_RIGHT = (
    Ellipse((85, 65, 113, 95), fill=AVATAR_BELLY),
    Ellipse((96, 69, 110, 83), fill=AVATAR_BODY),
    Ellipse((147, 65, 175, 95), fill=AVATAR_BELLY),
    Ellipse((158, 69, 172, 83), fill=AVATAR_BODY),
)

_FLIPPER_RIGHT_WAVE_MID = Polygon(((215, 130), (244, 130), (228, 180), (202, 165)), fill=AVATAR_BODY)

FLIPPERS_WAVE_MID: tuple[Shape, Shape] = (FLIPPERS_DEFAULT[0], _FLIPPER_RIGHT_WAVE_MID)
FLIPPERS_WAVE_UP: tuple[Shape, Shape] = (FLIPPERS_DEFAULT[0], FLIPPERS_RAISED[1])
