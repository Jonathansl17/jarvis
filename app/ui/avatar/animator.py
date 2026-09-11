"""Advances the avatar's active frame on a timer; no Tk import — the widget
that owns it supplies the scheduler (shaped like `tkinter.Widget.after`).
"""

from collections.abc import Callable

from PIL.Image import Image

from app.emotion.protocol import Emotion
from app.ui.avatar.spec import POSES, AvatarState

RenderFrame = Callable[[AvatarState, int, Emotion | None], Image]
Schedule = Callable[[int, Callable[[], None]], object]


class AvatarAnimator:
    """Owns the active `(state, frame_index)` and re-renders it on a timer."""

    def __init__(self, schedule: Schedule, render: RenderFrame, on_frame: Callable[[Image], None]) -> None:
        self._schedule = schedule
        self._render = render
        self._on_frame = on_frame
        self._state = AvatarState.IDLE
        self._emotion: Emotion | None = None
        self._frame_index = 0
        self._stopped = False

    def set_state(self, state: AvatarState) -> None:
        """Switch behavioral state, restarting its animation from frame 0."""
        self._state = state
        self._frame_index = 0
        self._render_and_reschedule()

    def set_emotion(self, emotion: Emotion | None) -> None:
        """Update the emotion overlaid on whatever state is currently active."""
        self._emotion = emotion
        self._on_frame(self._render(self._state, self._frame_index, self._emotion))

    def stop(self) -> None:
        """Stop scheduling further frames."""
        self._stopped = True

    def _render_and_reschedule(self) -> None:
        """Render the current frame and arm the timer for the next one."""
        if self._stopped:
            return
        image = self._render(self._state, self._frame_index, self._emotion)
        self._on_frame(image)
        pose = POSES[self._state][self._frame_index]
        self._schedule(pose.duration_ms, self._advance)

    def _advance(self) -> None:
        """Move to the next frame in the current state's loop, then render it."""
        frame_count = len(POSES[self._state])
        self._frame_index = (self._frame_index + 1) % frame_count
        self._render_and_reschedule()
