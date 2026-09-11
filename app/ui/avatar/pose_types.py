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
class PenguinPose:
    """One fully resolved animation frame for a given `AvatarState`.

    `body` defaults to the static torso ellipse; idle's breathing frames
    override it with a scaled copy instead of retyping its coordinates.
    `vertical_offset_px`/`horizontal_offset_px` shift every shape in the
    frame (the speaking bounce, the post-reply hop, fear's idle jitter)
    without retyping coordinates either.
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
