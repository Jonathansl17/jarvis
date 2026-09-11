"""Penguin poses per state/frame, from `gui-design.md` §7's frame tables.

`avatar.shapes` holds the drawable primitives and static/reusable shapes;
this module only assembles them into per-state, per-frame `PenguinPose`s.
"""

from dataclasses import dataclass
from enum import StrEnum

from app.ui.avatar.shapes import (
    BEAK_CLOSED,
    BEAK_HALF_OPEN,
    BEAK_OPEN,
    EYES_BLINK,
    EYES_OPEN,
    EYES_THINKING,
    FLIPPERS_DEFAULT,
    FLIPPERS_RAISED,
    Shape,
    dot_row,
    glow_ring,
)


class AvatarState(StrEnum):
    """The behavioral states the avatar's frames render, per §7."""

    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"


@dataclass(frozen=True)
class PenguinPose:
    """One fully resolved animation frame for a given `AvatarState`."""

    duration_ms: int
    glow_ring: Shape | None
    flippers: tuple[Shape, Shape]
    eyes: tuple[Shape, ...]
    beak: tuple[Shape, ...]
    extra: tuple[Shape, ...] = ()


def _idle_pose(duration_ms: int, eyes: tuple[Shape, ...]) -> PenguinPose:
    return PenguinPose(duration_ms, None, FLIPPERS_DEFAULT, eyes, BEAK_CLOSED)


def _listening_pose(duration_ms: int, ring_opacity: int) -> PenguinPose:
    return PenguinPose(duration_ms, glow_ring(ring_opacity), FLIPPERS_RAISED, EYES_OPEN, BEAK_CLOSED)


def _speaking_pose(duration_ms: int, beak: tuple[Shape, ...]) -> PenguinPose:
    return PenguinPose(duration_ms, None, FLIPPERS_DEFAULT, EYES_OPEN, beak)


# Idle: A (eyes open, 4700ms) -> B (blink, 300ms), looping ~5000ms per §7.
_IDLE_FRAMES = (_idle_pose(4700, EYES_OPEN), _idle_pose(300, EYES_BLINK))

# Listening: glow ring alpha 40%->100%->40%, discretized into 3 equal frames
# summing to the spec's 900ms pulse period.
_LISTENING_FRAMES = (
    _listening_pose(300, 0x66),
    _listening_pose(300, 0xFF),
    _listening_pose(300, 0x66),
)

# Thinking: 3 frames x 400ms, one dot fully lit per frame.
_THINKING_FRAMES = tuple(
    PenguinPose(400, None, FLIPPERS_DEFAULT, EYES_THINKING, BEAK_CLOSED, extra=dot_row(i))
    for i in range(3)
)

# Speaking: closed -> half-open -> open -> half-open, 4 x 150ms, looping
# back to closed (§7's 5-step description is this 4-frame cycle).
_SPEAKING_FRAMES = (
    _speaking_pose(150, BEAK_CLOSED),
    _speaking_pose(150, BEAK_HALF_OPEN),
    _speaking_pose(150, BEAK_OPEN),
    _speaking_pose(150, BEAK_HALF_OPEN),
)

POSES: dict[AvatarState, tuple[PenguinPose, ...]] = {
    AvatarState.IDLE: _IDLE_FRAMES,
    AvatarState.LISTENING: _LISTENING_FRAMES,
    AvatarState.THINKING: _THINKING_FRAMES,
    AvatarState.SPEAKING: _SPEAKING_FRAMES,
}
