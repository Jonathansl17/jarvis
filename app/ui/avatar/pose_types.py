"""Core avatar animation types: the behavioral-state enum and one resolved
animation frame (`PenguinPose`).

Split out of `spec.py` so the per-state frame-table modules
(`idle_frames.py`, `reactive_frames.py`) can depend on these two types
without importing `spec.py` itself and creating an import cycle — `spec.py`
imports *them* to assemble `POSES`.
"""

from dataclasses import dataclass
from enum import StrEnum

from app.ui.avatar.shapes import BODY, Shape


class AvatarState(StrEnum):
    """The behavioral states the avatar's frames render, per §7."""

    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"


@dataclass(frozen=True)
class CheekPulse:
    """A per-frame override of an expression's default cheek look — an
    emotion's idle loop pulsing or swelling its cheeks on specific frames
    without needing a distinct `Expression` per frame.
    """

    scale: float
    opacity: int


@dataclass(frozen=True)
class PenguinPose:
    """One fully resolved animation frame for a given `AvatarState`.

    `body` defaults to the static torso ellipse; idle's breathing frames
    override it with a scaled copy instead of retyping its coordinates.
    `vertical_offset_px`/`horizontal_offset_px` shift every shape in the
    frame (the speaking bounce, the post-reply hop, fear's idle jitter)
    without retyping coordinates either.

    The `*_override` fields let one frame of an emotion's own idle loop
    momentarily replace part of that emotion's `Expression` (e.g. happy's
    eye squint at the peak of a bounce, fear's darting pupils, angry's
    eyebrow twitch) — `None` means "keep the expression's usual look".

    `replace_expression_extra`, when set, drops the expression's own static
    decoration (sad's tear, fear's sweat, disgust's tongue, surprise's
    exclamation mark) for this frame so `extra` can hold an animated
    stand-in (sliding, extending, popping in) without both being drawn at
    once.
    """

    duration_ms: int
    glow_ring: Shape | None
    flippers: tuple[Shape, Shape]
    eyes: tuple[Shape, ...]
    beak: tuple[Shape, ...]
    extra: tuple[Shape, ...] = ()
    body: Shape = BODY
    vertical_offset_px: int = 0
    horizontal_offset_px: int = 0
    eyes_override: tuple[Shape, ...] | None = None
    flippers_override: tuple[Shape, Shape] | None = None
    eyebrows_override: tuple[Shape, ...] | None = None
    cheek: CheekPulse | None = None
    replace_expression_extra: bool = False
