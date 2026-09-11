"""Advances the avatar's active frame on a timer; no Tk import — the widget
that owns it supplies the scheduler (shaped like `tkinter.Widget.after`).

Idle is not a plain loop: on top of its breathing cycle, this animator
splices in a blink, a flipper wave, a one-shot post-reply hop, and a
reaction transition on emotion change (see `set_emotion`). All are still
addressed as indices into `POSES[AvatarState.IDLE]` (`idle_frames.py`), so
every frame stays cached by the same `(state, index, emotion)` key the
renderer already uses for a plain loop.
"""

from collections.abc import Callable

from PIL.Image import Image

from app.emotion.protocol import Emotion
from app.ui.avatar.emotion_display import displayed_emotion
from app.ui.avatar.emotion_poses import IDLE_LOOP_FOR_EMOTION
from app.ui.avatar.idle_timers import BLINK_EVENT, WAVE_EVENT, IdleTimers
from app.ui.avatar.spec import (
    IDLE_BLINK_INDEX,
    IDLE_BREATHE_FRAME_COUNT,
    IDLE_HOP_FRAME_COUNT,
    IDLE_HOP_START_INDEX,
    IDLE_TRANSITION_FRAME_COUNT,
    IDLE_TRANSITION_START_INDEX,
    IDLE_WAVE_FRAME_COUNT,
    IDLE_WAVE_START_INDEX,
    POSES,
    AvatarState,
)

RenderFrame = Callable[[AvatarState, int, Emotion | None], Image]
Schedule = Callable[[int, Callable[[], None]], object]


class AvatarAnimator:
    """Owns the active `(state, frame_index)` and re-renders it on a timer."""

    def __init__(self, schedule: Schedule, render: RenderFrame, on_frame: Callable[[Image], None]) -> None:
        self._schedule = schedule
        self._render = render
        self._on_frame = on_frame
        self._emotion: Emotion | None = None
        self._stopped = False
        self._playing_event = False
        self._event_indices: list[int] = []
        self._idle_timers = IdleTimers()
        self._reset_for_state(AvatarState.IDLE)

    def set_state(self, state: AvatarState) -> None:
        """Switch behavioral state, restarting its animation from frame 0."""
        self._reset_for_state(state)
        self._render_and_reschedule()

    def set_emotion(self, emotion: Emotion | None) -> None:
        """Update the emotion overlaid on the current state; if idle and the
        *displayed* emotion actually changes, play a reaction transition
        first instead of cutting straight to the new loop."""
        previous_displayed = displayed_emotion(self._emotion)
        self._emotion = emotion
        if self._should_play_transition(previous_displayed):
            self._start_event(IDLE_TRANSITION_START_INDEX, IDLE_TRANSITION_FRAME_COUNT)
        elif self._state is AvatarState.IDLE and not self._playing_event:
            self._frame_index, _ = self._active_idle_loop()
        self._on_frame(self._render(self._state, self._frame_index, self._emotion))

    def _should_play_transition(self, previous_displayed: Emotion | None) -> bool:
        """Whether a reaction transition should play: only while idle, only
        when not already mid-event, and only on an actual display change."""
        return (
            self._state is AvatarState.IDLE
            and not self._playing_event
            and displayed_emotion(self._emotion) != previous_displayed
        )

    def play_hop_then_idle(self) -> None:
        """Play the one-time post-reply hop, then settle into idle breathing."""
        self._reset_for_state(AvatarState.IDLE)
        self._start_event(IDLE_HOP_START_INDEX, IDLE_HOP_FRAME_COUNT)
        self._render_and_reschedule()

    def stop(self) -> None:
        """Stop scheduling further frames."""
        self._stopped = True

    def _reset_for_state(self, state: AvatarState) -> None:
        """Reset per-state counters/timers without rendering yet."""
        self._state = state
        self._frame_index = 0
        self._playing_event = False
        if state is AvatarState.IDLE:
            self._frame_index, _ = self._active_idle_loop()
            self._idle_timers.reset()

    def _active_idle_loop(self) -> tuple[int, int]:
        """Return the `(start_index, frame_count)` idle loop the current
        displayed emotion drives: breathing by default, or that emotion's
        own loop (see `emotion_poses.IDLE_LOOP_FOR_EMOTION`)."""
        loop = IDLE_LOOP_FOR_EMOTION.get(displayed_emotion(self._emotion))
        return (loop.start_index, loop.frame_count) if loop is not None else (0, IDLE_BREATHE_FRAME_COUNT)

    def _render_and_reschedule(self) -> None:
        """Render the current frame and arm the timer for the next one."""
        if self._stopped:
            return
        image = self._render(self._state, self._frame_index, self._emotion)
        self._on_frame(image)
        duration_ms = POSES[self._state][self._frame_index].duration_ms
        self._schedule(duration_ms, lambda: self._advance(duration_ms))

    def _advance(self, elapsed_ms: int) -> None:
        """Move to the next frame: an event step, an idle tick, or a plain loop."""
        if self._playing_event:
            self._advance_event()
        elif self._state is AvatarState.IDLE:
            self._advance_idle(elapsed_ms)
        else:
            frame_count = len(POSES[self._state])
            self._frame_index = (self._frame_index + 1) % frame_count
        self._render_and_reschedule()

    def _advance_event(self) -> None:
        """Step through a spliced-in event (blink/wave/hop), then resume
        whichever idle loop (breathing, or the current emotion's own) was
        playing before the event started."""
        if self._event_indices:
            self._frame_index = self._event_indices.pop(0)
        else:
            self._playing_event = False
            self._frame_index, _ = self._active_idle_loop()

    def _advance_idle(self, elapsed_ms: int) -> None:
        """Tick idle's active loop, triggering a blink or wave when due."""
        due_event = self._idle_timers.tick(elapsed_ms)
        if due_event == BLINK_EVENT:
            self._start_event(IDLE_BLINK_INDEX, 1)
        elif due_event == WAVE_EVENT:
            self._start_event(IDLE_WAVE_START_INDEX, IDLE_WAVE_FRAME_COUNT)
        else:
            start, count = self._active_idle_loop()
            self._frame_index = start + (self._frame_index - start + 1) % count

    def _start_event(self, start_index: int, frame_count: int) -> None:
        """Begin playing `frame_count` frames starting at `start_index`."""
        self._playing_event = True
        self._event_indices = list(range(start_index + 1, start_index + frame_count))
        self._frame_index = start_index
