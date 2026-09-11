"""Per-emotion eyes/beak/flipper shape overrides, from the expression table.

Split out of `expressions.py` to stay within the project's file-size limit;
`expressions.py` only assembles these into the `EXPRESSIONS` table. Eyebrows
have their own module, `eyebrows.py`, since they are a distinct face part.
"""

from app.ui.avatar.shapes import (
    AVATAR_BEAK_ANGRY,
    AVATAR_BEAK_FOOT,
    AVATAR_BELLY,
    AVATAR_BODY,
    FLIPPERS_DEFAULT,
    Ellipse,
    Line,
    Polygon,
    Shape,
)

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

# Eye overrides, one per emotion row; neutral keeps the pose's own default
# open eyes.

# Closed and smiling: an upward arc (a "^" caret) over a light eye patch so
# it reads against the head's own dark color, approximated with a 3-point
# line since `Shape` has no arc/pieslice primitive.
HAPPY_EYES = (
    Ellipse((84, 68, 114, 92), fill=AVATAR_BELLY),
    Line(((87, 88), (99, 76), (111, 88)), fill=AVATAR_BODY, width=4),
    Ellipse((146, 68, 176, 92), fill=AVATAR_BELLY),
    Line(((149, 88), (161, 76), (173, 88)), fill=AVATAR_BODY, width=4),
)
# Half closed, with a drooping upper eyelid covering the top of each eye.
SAD_EYES = (
    Ellipse((85, 65, 113, 95), fill=AVATAR_BELLY),
    Ellipse((92, 76, 106, 90), fill=AVATAR_BODY),
    Ellipse((147, 65, 175, 95), fill=AVATAR_BELLY),
    Ellipse((154, 76, 168, 90), fill=AVATAR_BODY),
    Polygon(((84, 65), (114, 65), (114, 79), (84, 74)), fill=AVATAR_BODY),
    Polygon(((146, 65), (176, 65), (176, 74), (146, 79)), fill=AVATAR_BODY),
)
ANGRY_EYES = (
    Ellipse((85, 70, 113, 90), fill=AVATAR_BELLY),
    Ellipse((92, 73, 106, 87), fill=AVATAR_BODY),
    Ellipse((147, 70, 175, 90), fill=AVATAR_BELLY),
    Ellipse((154, 73, 168, 87), fill=AVATAR_BODY),
)
SURPRISE_EYES = (
    Ellipse((82, 63, 116, 97), fill=AVATAR_BELLY),
    Ellipse((95, 76, 103, 84), fill=AVATAR_BODY),
    Ellipse((144, 63, 178, 97), fill=AVATAR_BELLY),
    Ellipse((157, 76, 165, 84), fill=AVATAR_BODY),
)
# Pupils shifted toward one side within their sclera, so both eyes read as
# "looking away" rather than straight ahead.
FEAR_EYES = (
    Ellipse((85, 65, 113, 95), fill=AVATAR_BELLY),
    Ellipse((99, 76, 107, 84), fill=AVATAR_BODY),
    Ellipse((147, 65, 175, 95), fill=AVATAR_BELLY),
    Ellipse((152, 76, 160, 84), fill=AVATAR_BODY),
)
# One eye squinted shut: a light patch (so the line reads against the dark
# head) with a closed-eye line over it.
DISGUST_EYES = (
    Ellipse((85, 65, 113, 95), fill=AVATAR_BELLY),
    Ellipse((92, 73, 106, 87), fill=AVATAR_BODY),
    Ellipse((147, 74, 175, 86), fill=AVATAR_BELLY),
    Line(((149, 80), (173, 80)), fill=AVATAR_BODY, width=3),
)

