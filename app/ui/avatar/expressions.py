"""Emotion -> eyes/beak/eyebrow/flipper/cheek overrides, from §9's per-emotion
table, plus the webcam-emotion-to-avatar-reaction mirroring policy (§7's
"Mirroring policy" box).

`map_emotion_to_avatar()` is the one function that may branch on emotion
strings for this mapping — nothing else special-cases it, per the design
spec's explicit instruction. Per-emotion shape constants live in
`expression_shapes.py`, split out to stay within the file-size limit.
"""

from dataclasses import dataclass

from app.emotion.protocol import Emotion
from app.ui.avatar import expression_shapes as shapes
from app.ui.avatar.shapes import Shape, beak_open, cheek_shapes

_CHEEK_OPACITY_DEFAULT = 102  # 40% of 255, the design spec's cheek token alpha.
_CHEEK_OPACITY_HAPPY = 255
_CHEEK_OPACITY_SUPPRESSED = 0

# Detected emotion -> what the avatar shows; angry/disgust never reflect
# back at the user, per §7's mirroring policy.
_AVATAR_EMOTION_FOR: dict[Emotion, Emotion] = {
    Emotion.HAPPY: Emotion.HAPPY,
    Emotion.SAD: Emotion.SAD,
    Emotion.SURPRISE: Emotion.SURPRISE,
    Emotion.FEAR: Emotion.SURPRISE,
    Emotion.NEUTRAL: Emotion.NEUTRAL,
    Emotion.ANGRY: Emotion.NEUTRAL,
    Emotion.DISGUST: Emotion.NEUTRAL,
}


def map_emotion_to_avatar(emotion: Emotion) -> Emotion:
    """Return the emotion the avatar should display for a detected `emotion`."""
    return _AVATAR_EMOTION_FOR[emotion]


@dataclass(frozen=True)
class Expression:
    """Overrides a pose's default eyes/beak/eyebrows/flippers/cheeks."""

    eyes: tuple[Shape, ...] | None = None
    eyebrows: tuple[Shape, ...] = ()
    beak: tuple[Shape, ...] | None = None
    flippers: tuple[Shape, Shape] | None = None
    cheek_opacity: int = _CHEEK_OPACITY_DEFAULT


EXPRESSIONS: dict[Emotion, Expression] = {
    Emotion.HAPPY: Expression(beak=shapes.HAPPY_BEAK, cheek_opacity=_CHEEK_OPACITY_HAPPY),
    Emotion.SAD: Expression(
        eyes=shapes.SAD_EYES,
        eyebrows=shapes.eyebrows(((85, 57), (113, 51)), ((147, 51), (175, 57))),
        beak=shapes.SAD_BEAK,
        flippers=shapes.FLIPPERS_DROOPING,
    ),
    Emotion.ANGRY: Expression(
        eyes=shapes.ANGRY_EYES,
        eyebrows=shapes.eyebrows(((85, 60), (113, 50)), ((147, 50), (175, 60))),
        beak=shapes.ANGRY_BEAK,
        flippers=shapes.FLIPPERS_ANGRY,
        cheek_opacity=_CHEEK_OPACITY_SUPPRESSED,
    ),
    Emotion.SURPRISE: Expression(
        eyes=shapes.SURPRISE_EYES,
        eyebrows=shapes.eyebrows(((85, 53), (113, 53)), ((147, 53), (175, 53))),
        beak=beak_open(14),
        flippers=shapes.FLIPPERS_OUT,
    ),
    Emotion.FEAR: Expression(
        eyes=shapes.FEAR_EYES,
        eyebrows=shapes.eyebrows(((85, 57), (113, 45)), ((147, 45), (175, 57))),
        beak=shapes.FEAR_BEAK,
        flippers=shapes.FLIPPERS_TIGHT,
        cheek_opacity=_CHEEK_OPACITY_SUPPRESSED,
    ),
    Emotion.DISGUST: Expression(
        eyes=shapes.DISGUST_EYES,
        eyebrows=shapes.eyebrow(((147, 55), (175, 70))),
        beak=shapes.DISGUST_BEAK,
        flippers=shapes.FLIPPERS_DISGUST,
        cheek_opacity=_CHEEK_OPACITY_SUPPRESSED,
    ),
    Emotion.NEUTRAL: Expression(),
}


def resolve_expression(emotion: Emotion) -> Expression:
    """Return the `Expression` for `emotion`, applying the mirroring policy."""
    return EXPRESSIONS[map_emotion_to_avatar(emotion)]


def cheeks_for(expression: Expression | None) -> tuple[Shape, ...]:
    """Return the cheek shapes an expression asks for (default if `None`)."""
    opacity = expression.cheek_opacity if expression is not None else _CHEEK_OPACITY_DEFAULT
    return cheek_shapes(opacity)
