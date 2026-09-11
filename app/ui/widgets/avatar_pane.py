"""Renders the current avatar frame and its emotion overlay (§7)."""

import random

from textual.widgets import Static

from app.emotion.protocol import Emotion
from app.ui.emotion_overlay import apply_emotion_overlay
from app.ui.frames import AVATAR_FRAMES, AvatarState

_IDLE_BLINK_HOLD_SECONDS = 0.150
_IDLE_BLINK_INTERVAL_RANGE_SECONDS = (6.0, 9.0)
_THINKING_FRAME_INTERVAL_SECONDS = 0.3
_SPEAKING_FRAME_INTERVAL_SECONDS = 0.12
_LISTENING_EAR_PULSE_SECONDS = 0.4


class AvatarPane(Static):
    """Owns the avatar's animation timers and its last known emotion overlay."""

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._state = AvatarState.IDLE
        self._emotion: Emotion | None = None
        self._frame_index = 0
        self._timer = None

    def on_mount(self) -> None:
        self.set_state(AvatarState.IDLE)

    def set_state(self, state: AvatarState) -> None:
        """Switch behavioral state, restarting that state's animation timer."""
        self._state = state
        self._frame_index = 0
        self._restart_timer()
        self._render_current_frame()

    def set_emotion(self, emotion: Emotion | None) -> None:
        """Update the emotion overlaid on whatever state is currently active."""
        self._emotion = emotion
        self._render_current_frame()

    def _restart_timer(self) -> None:
        """Replace the running animation timer with the one `self._state` needs."""
        if self._timer is not None:
            self._timer.stop()
        schedulers = {
            AvatarState.IDLE: self._schedule_idle_tick,
            AvatarState.THINKING: lambda: self.set_interval(
                _THINKING_FRAME_INTERVAL_SECONDS, self._advance_frame
            ),
            AvatarState.SPEAKING: lambda: self.set_interval(
                _SPEAKING_FRAME_INTERVAL_SECONDS, self._advance_frame
            ),
            AvatarState.LISTENING: lambda: self.set_interval(
                _LISTENING_EAR_PULSE_SECONDS, self._advance_frame
            ),
        }
        self._timer = schedulers[self._state]()

    def _schedule_idle_tick(self):
        """Hold the open-eyes frame, then blink once after a randomized wait."""
        interval = random.uniform(*_IDLE_BLINK_INTERVAL_RANGE_SECONDS)
        return self.set_timer(interval, self._blink_then_reschedule)

    def _blink_then_reschedule(self) -> None:
        """Show the blink frame briefly, then resume the idle schedule."""
        self._frame_index = 1
        self._render_current_frame()
        self.set_timer(_IDLE_BLINK_HOLD_SECONDS, self._end_blink)

    def _end_blink(self) -> None:
        """Return to the open-eyes frame and arm the next blink."""
        self._frame_index = 0
        self._render_current_frame()
        self._timer = self._schedule_idle_tick()

    def _advance_frame(self) -> None:
        """Move to the next frame in the current state's loop and render it."""
        frames = AVATAR_FRAMES[self._state]
        self._frame_index = (self._frame_index + 1) % len(frames)
        self._render_current_frame()

    def _render_current_frame(self) -> None:
        """Draw the active frame, with the emotion overlay applied if any."""
        frame = AVATAR_FRAMES[self._state][self._frame_index]
        if self._emotion is not None:
            frame = apply_emotion_overlay(frame, self._emotion)
        self.update(frame)
