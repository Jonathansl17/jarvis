"""Drawable primitives and the static/reusable penguin shapes, from
`gui-design.md` §7, verbatim.

Colors here are the subset of the design spec's §4 tokens the avatar draws
with; duplicated as plain hex strings (rather than imported from
`ui.theme`) so this module stays free of any `customtkinter` import — see
the architecture plan's "dependency direction" section.
"""

from dataclasses import dataclass

AVATAR_BODY = "#1C2530"
AVATAR_BELLY = "#F4F6F8"
AVATAR_BELLY_SAD = "#E1E4E8"
AVATAR_BEAK_FOOT = "#FF9F1C"
AVATAR_BEAK_ANGRY = "#E07A00"
AVATAR_CHEEK = "#FF9E9E"
AVATAR_CHEEK_ANGRY = "#FF4D4F"
AVATAR_CHEEK_DISGUST = "#B7D69A"
ACCENT_PRIMARY = "#2DE2C9"

CANVAS_SIZE_PX = 260
_CHEEK_RADIUS_PX = 11


@dataclass(frozen=True)
class Ellipse:
    box: tuple[int, int, int, int]
    fill: str | None = None
    outline: str | None = None
    width: int = 0


@dataclass(frozen=True)
class Polygon:
    points: tuple[tuple[int, int], ...]
    fill: str


@dataclass(frozen=True)
class Line:
    points: tuple[tuple[int, int], ...]
    fill: str
    width: int = 3


Shape = Ellipse | Polygon | Line


def cheek_shapes(opacity: int, fill: str = AVATAR_CHEEK, scale: float = 1.0) -> tuple[Shape, ...]:
    """Return the two cheek ellipses at `opacity` (0-255), `fill`-colored and
    scaled by `scale` (happy's cheeks are larger than the other emotions').
    """
    if opacity <= 0:
        return ()
    radius = round(_CHEEK_RADIUS_PX * scale)
    color = f"{fill}{opacity:02x}"
    return (
        Ellipse((93 - radius, 100 - radius, 93 + radius, 100 + radius), fill=color),
        Ellipse((167 - radius, 100 - radius, 167 + radius, 100 + radius), fill=color),
    )


# Static back-to-front layers drawn on every frame, per §7 items 2-4 (feet
# drawn first, per the draw-order note, so only their tips peek past body).
FEET = (
    Ellipse((88, 232, 122, 254), fill=AVATAR_BEAK_FOOT),
    Ellipse((138, 232, 172, 254), fill=AVATAR_BEAK_FOOT),
)
BODY = Ellipse((40, 55, 220, 250), fill=AVATAR_BODY)
HEAD = Ellipse((60, 15, 200, 140), fill=AVATAR_BODY)
BELLY = Ellipse((80, 105, 180, 240), fill=AVATAR_BELLY)


def belly_shape(fill: str = AVATAR_BELLY) -> Shape:
    """Return the belly ellipse tinted `fill` (sad's slightly grey belly)."""
    return Ellipse(BELLY.box, fill=fill)

FLIPPERS_DEFAULT = (
    Polygon(((45, 140), (18, 175), (30, 215), (55, 190)), fill=AVATAR_BODY),
    Polygon(((215, 140), (242, 175), (230, 215), (205, 190)), fill=AVATAR_BODY),
)
FLIPPERS_RAISED = (
    Polygon(((45, 120), (15, 90), (35, 60), (60, 110)), fill=AVATAR_BODY),
    Polygon(((215, 120), (245, 90), (225, 60), (200, 110)), fill=AVATAR_BODY),
)

EYES_OPEN = (
    Ellipse((85, 65, 113, 95), fill=AVATAR_BELLY),
    Ellipse((92, 73, 106, 87), fill=AVATAR_BODY),
    Ellipse((147, 65, 175, 95), fill=AVATAR_BELLY),
    Ellipse((154, 73, 168, 87), fill=AVATAR_BODY),
)
EYES_BLINK = (
    Line(((85, 80), (113, 80)), fill=AVATAR_BODY, width=3),
    Line(((147, 80), (175, 80)), fill=AVATAR_BODY, width=3),
)
EYES_THINKING = (
    Ellipse((85, 65, 113, 95), fill=AVATAR_BELLY),
    Ellipse((92, 69, 106, 83), fill=AVATAR_BODY),
    Ellipse((147, 65, 175, 95), fill=AVATAR_BELLY),
    Ellipse((154, 69, 168, 83), fill=AVATAR_BODY),
)

BEAK_CLOSED = (Polygon(((116, 100), (144, 100), (130, 118)), fill=AVATAR_BEAK_FOOT),)

# The round "open beak" builder (`beak_round_open`) and its two open sizes
# (`BEAK_HALF_OPEN`/`BEAK_OPEN`) live in `beak_shapes.py`, split out to stay
# within this module's file-size limit.

_DOT_ROW_Y = 175
_DOT_RADIUS = 4
_DOT_X = (115, 130, 145)
_DOT_FULL_OPACITY = "CC"
_DOT_LOW_OPACITY = "4D"


def dot_row(active_index: int) -> tuple[Shape, ...]:
    """The thinking state's 3-dot row, one dot fully lit per frame (§7)."""
    return tuple(
        Ellipse(
            (x - _DOT_RADIUS, _DOT_ROW_Y - _DOT_RADIUS, x + _DOT_RADIUS, _DOT_ROW_Y + _DOT_RADIUS),
            fill=f"{AVATAR_BODY}{_DOT_FULL_OPACITY if i == active_index else _DOT_LOW_OPACITY}",
        )
        for i, x in enumerate(_DOT_X)
    )


def glow_ring(opacity: int) -> Shape:
    """The listening-state glow ring at `opacity` (0-255), per §7 item 1."""
    return Ellipse((5, 5, 255, 255), outline=f"{ACCENT_PRIMARY}{opacity:02x}", width=4)
