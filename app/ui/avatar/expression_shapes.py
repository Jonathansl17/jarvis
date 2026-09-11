"""Per-emotion eyes/beak/eyebrow/flipper shape overrides, from §9's table.

Split out of `expressions.py` to stay within the project's file-size limit;
`expressions.py` only assembles these into the `EXPRESSIONS` table.
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


def eyebrows(left: tuple[tuple[int, int], ...], right: tuple[tuple[int, int], ...]) -> tuple[Shape, ...]:
    """Build a pair of 4px-wide eyebrow lines, per §7 item 9."""
    return (Line(left, fill=AVATAR_BODY, width=4), Line(right, fill=AVATAR_BODY, width=4))


def eyebrow(points: tuple[tuple[int, int], ...]) -> tuple[Shape, ...]:
    """Build a single 4px-wide eyebrow line (disgust draws only one, per §9)."""
    return (Line(points, fill=AVATAR_BODY, width=4),)


HAPPY_BEAK = (Polygon(((112, 100), (148, 100), (130, 118)), fill=AVATAR_BEAK_FOOT),)
SAD_BEAK = (Polygon(((120, 100), (140, 100), (115, 120)), fill=AVATAR_BEAK_FOOT),)
ANGRY_BEAK = (Polygon(((116, 100), (144, 100), (130, 118)), fill=AVATAR_BEAK_ANGRY),)
FEAR_BEAK = (Polygon(((122, 100), (138, 100), (130, 112)), fill=AVATAR_BEAK_FOOT),)
DISGUST_BEAK = (Polygon(((110, 105), (144, 100), (128, 118)), fill=AVATAR_BEAK_FOOT),)

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
FLIPPERS_TIGHT = (
    Polygon(((53, 140), (35, 170), (42, 205), (58, 190)), fill=AVATAR_BODY),
    Polygon(((207, 140), (225, 170), (218, 205), (202, 190)), fill=AVATAR_BODY),
)
FLIPPERS_DISGUST = (FLIPPERS_DEFAULT[0], FLIPPERS_OUT[1])

# Eye overrides, one per §9 row; happy/neutral keep the pose's own default
# eyes — happy's "upper-half sclera" detail is approximated by the default
# open eyes, since `Shape` has no pieslice primitive.
SAD_EYES = (
    Ellipse((85, 65, 113, 95), fill=AVATAR_BELLY),
    Ellipse((92, 76, 106, 90), fill=AVATAR_BODY),
    Ellipse((147, 65, 175, 95), fill=AVATAR_BELLY),
    Ellipse((154, 76, 168, 90), fill=AVATAR_BODY),
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
FEAR_EYES = (
    Ellipse((85, 65, 113, 95), fill=AVATAR_BELLY),
    Ellipse((98, 76, 106, 84), fill=AVATAR_BODY),
    Ellipse((147, 65, 175, 95), fill=AVATAR_BELLY),
    Ellipse((151, 76, 159, 84), fill=AVATAR_BODY),
)
DISGUST_EYES = (
    Ellipse((85, 65, 113, 95), fill=AVATAR_BELLY),
    Ellipse((92, 73, 106, 87), fill=AVATAR_BODY),
    Line(((147, 80), (175, 80)), fill=AVATAR_BODY, width=3),
)
