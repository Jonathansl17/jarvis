"""Assembles the per-state pose tables into `POSES`, and re-exports
`AvatarState`/`PenguinPose` for the rest of the avatar package.

`idle_frames.py` and `reactive_frames.py` hold each state's actual frame
detail; this module only combines them, per `gui-design.md` §7.
"""

from app.ui.avatar.idle_frames import (
    IDLE_BLINK_INDEX,
    IDLE_BREATHE_FRAME_COUNT,
    IDLE_FRAMES,
    IDLE_HOP_FRAME_COUNT,
    IDLE_HOP_START_INDEX,
    IDLE_WAVE_FRAME_COUNT,
    IDLE_WAVE_START_INDEX,
)
from app.ui.avatar.pose_types import AvatarState, PenguinPose
from app.ui.avatar.reactive_frames import LISTENING_FRAMES, SPEAKING_FRAMES, THINKING_FRAMES

POSES: dict[AvatarState, tuple[PenguinPose, ...]] = {
    AvatarState.IDLE: IDLE_FRAMES,
    AvatarState.LISTENING: LISTENING_FRAMES,
    AvatarState.THINKING: THINKING_FRAMES,
    AvatarState.SPEAKING: SPEAKING_FRAMES,
}

__all__ = [
    "AvatarState",
    "PenguinPose",
    "POSES",
    "IDLE_BLINK_INDEX",
    "IDLE_BREATHE_FRAME_COUNT",
    "IDLE_HOP_FRAME_COUNT",
    "IDLE_HOP_START_INDEX",
    "IDLE_WAVE_FRAME_COUNT",
    "IDLE_WAVE_START_INDEX",
]
