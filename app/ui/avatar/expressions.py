"""Emotion -> full-body pose overrides (eyes/beak/eyebrows/flippers/cheeks/
belly/body offset-scale/extra decorations), from the expression table.

The mirroring policy (which emotion the avatar displays, and which trigger
its post-reply hop) lives in `mirroring.py`; this module re-exports
`map_emotion_to_avatar`/`HOP_TRIGGER_EMOTIONS` so callers only need one
import. Per-emotion shape constants live in `expression_shapes.py`/
`eyebrows.py`/`decorations.py`, and per-emotion body pose data in
`emotion_poses.py`, split out to stay within the file-size limit.
"""

from dataclasses import dataclass

from app.emotion.protocol import Emotion
from app.ui.avatar import decorations, eyebrows
from app.ui.avatar import expression_shapes as shapes
from app.ui.avatar.beak_shapes import beak_round_open
from app.ui.avatar.emotion_poses import BODY_POSES, BodyPose
from app.ui.avatar.mirroring import HOP_TRIGGER_EMOTIONS, map_emotion_to_avatar
from app.ui.avatar.pose_types import CheekPulse
from app.ui.avatar.shapes import (
    AVATAR_BELLY,
    AVATAR_BELLY_SAD,
    AVATAR_CHEEK,
    AVATAR_CHEEK_ANGRY,
    AVATAR_CHEEK_DISGUST,
    FLIPPERS_RAISED,
    Shape,
    cheek_shapes,
)

_SURPRISE_BEAK_WIDTH_PX = 22
_SURPRISE_BEAK_HEIGHT_PX = 26

__all__ = [
    "Expression",
    "EXPRESSIONS",
    "HOP_TRIGGER_EMOTIONS",
    "map_emotion_to_avatar",
    "resolve_expression",
    "cheeks_for",
]

_CHEEK_OPACITY_DEFAULT = 102  # 40% of 255, the design spec's cheek token alpha.
_CHEEK_OPACITY_HAPPY = 255
_CHEEK_OPACITY_VIVID = 220
_CHEEK_OPACITY_SUPPRESSED = 0
_CHEEK_SCALE_HAPPY = 1.4


@dataclass(frozen=True)
class Expression:
    """Overrides a pose's default eyes/beak/eyebrows/flippers/cheeks/belly,
    plus a whole-body offset/scale and any extra decorations."""

    eyes: tuple[Shape, ...] | None = None
    eyebrows: tuple[Shape, ...] = ()
    beak: tuple[Shape, ...] | None = None
    flippers: tuple[Shape, Shape] | None = None
    cheek_opacity: int = _CHEEK_OPACITY_DEFAULT
    cheek_fill: str = AVATAR_CHEEK
    cheek_scale: float = 1.0
    belly_fill: str = AVATAR_BELLY
    body: BodyPose = BodyPose()
    extra: tuple[Shape, ...] = ()


EXPRESSIONS: dict[Emotion, Expression] = {
    Emotion.HAPPY: Expression(
        eyes=shapes.HAPPY_EYES,
        beak=shapes.HAPPY_BEAK,
        flippers=FLIPPERS_RAISED,
        cheek_opacity=_CHEEK_OPACITY_HAPPY,
        cheek_scale=_CHEEK_SCALE_HAPPY,
        body=BODY_POSES[Emotion.HAPPY],
    ),
    Emotion.SAD: Expression(
        eyes=shapes.SAD_EYES,
        eyebrows=eyebrows.SAD_EYEBROWS,
        beak=shapes.SAD_BEAK,
        flippers=shapes.FLIPPERS_DROOPING,
        belly_fill=AVATAR_BELLY_SAD,
        body=BODY_POSES[Emotion.SAD],
        extra=decorations.TEAR_DROP,
    ),
    Emotion.ANGRY: Expression(
        eyes=shapes.ANGRY_EYES,
        eyebrows=eyebrows.ANGRY_EYEBROWS,
        beak=shapes.ANGRY_BEAK,
        flippers=shapes.FLIPPERS_ANGRY,
        cheek_opacity=_CHEEK_OPACITY_VIVID,
        cheek_fill=AVATAR_CHEEK_ANGRY,
        body=BODY_POSES[Emotion.ANGRY],
    ),
    Emotion.SURPRISE: Expression(
        eyes=shapes.SURPRISE_EYES,
        eyebrows=eyebrows.SURPRISE_EYEBROWS,
        beak=beak_round_open(_SURPRISE_BEAK_WIDTH_PX, _SURPRISE_BEAK_HEIGHT_PX),
        flippers=shapes.FLIPPERS_OUT,
        body=BODY_POSES[Emotion.SURPRISE],
        extra=decorations.EXCLAMATION_MARK,
    ),
    Emotion.FEAR: Expression(
        eyes=shapes.FEAR_EYES,
        eyebrows=eyebrows.FEAR_EYEBROWS,
        beak=shapes.FEAR_BEAK,
        flippers=shapes.FLIPPERS_COVER_FACE,
        cheek_opacity=_CHEEK_OPACITY_SUPPRESSED,
        body=BODY_POSES[Emotion.FEAR],
        extra=decorations.SWEAT_DROP,
    ),
    Emotion.DISGUST: Expression(
        eyes=shapes.DISGUST_EYES,
        eyebrows=eyebrows.DISGUST_EYEBROWS,
        beak=shapes.DISGUST_BEAK,
        flippers=shapes.FLIPPERS_DISGUST,
        cheek_opacity=_CHEEK_OPACITY_VIVID,
        cheek_fill=AVATAR_CHEEK_DISGUST,
        body=BODY_POSES[Emotion.DISGUST],
        extra=decorations.TONGUE,
    ),
    Emotion.NEUTRAL: Expression(),
}


def resolve_expression(emotion: Emotion) -> Expression:
    """Return the `Expression` for `emotion`, applying the mirroring policy."""
    return EXPRESSIONS[map_emotion_to_avatar(emotion)]


def cheeks_for(expression: Expression | None, pulse: CheekPulse | None = None) -> tuple[Shape, ...]:
    """Return the cheek shapes an expression asks for (default if `None`),
    or `pulse`'s scale/opacity instead when an idle-loop frame supplies one
    (an emotion's cheeks swelling or pulsing on specific frames)."""
    fill = expression.cheek_fill if expression is not None else AVATAR_CHEEK
    if pulse is not None:
        return cheek_shapes(pulse.opacity, fill, pulse.scale)
    if expression is None:
        return cheek_shapes(_CHEEK_OPACITY_DEFAULT, fill)
    return cheek_shapes(expression.cheek_opacity, fill, expression.cheek_scale)
