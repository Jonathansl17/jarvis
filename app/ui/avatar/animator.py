"""Advances the avatar's active frame on a timer; no Tk import — the widget
that owns it supplies the scheduler (shaped like `tkinter.Widget.after`).

Idle is not a plain loop: on top of its breathing cycle, this animator
splices in a randomly timed blink and a periodic flipper wave, and can play
a one-shot reaction (the post-reply hop) before resuming it. All three are
still addressed as indices into `POSES[AvatarState.IDLE]` (see
`idle_frames.py`), so every frame stays cached by the same
`(state, index, emotion)` key the renderer already uses for a plain loop.
"""

import random
from collections.abc import Callable

from PIL.Image import Image

from app.emotion.protocol import Emotion
from app.ui.avatar.emotion_poses import IDLE_LOOP_FOR_EMOTION
from app.ui.avatar.mirroring import map_emotion_to_avatar
from app.ui.avatar.spec import (
    IDLE_BLINK_INDEX,
    IDLE_BREATHE_FRAME_COUNT,
    IDLE_HOP_FRAME_COUNT,
    IDLE_HOP_START_INDEX,
    IDLE_WAVE_FRAME_COUNT,
    IDLE_WAVE_START_INDEX,
    POSES,
    AvatarState,
)

RenderFrame = Callable[[AvatarState, int, Emotion | None], Image]
Schedule = Callable[[int, Callable[[], None]], object]

_BLINK_INTERVAL_RANGE_MS = (4000, 7000)
_WAVE_INTERVAL_MS = 12000


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
        self._reset_for_state(AvatarState.IDLE)

    def set_state(self, state: AvatarState) -> None:
        """Switch behavioral state, restarting its animation from frame 0."""
        self._reset_for_state(state)
        self._render_and_reschedule()

    def set_emotion(self, emotion: Emotion | None) -> None:
        """Update the emotion overlaid on whatever state is currently active,
        re-centering idle's loop on the new emotion's own loop if it has one.
        """
        self._emotion = emotion
        if self._state is AvatarState.IDLE and not self._playing_event:
            self._frame_index, _ = self._active_idle_loop()
        self._on_frame(self._render(self._state, self._frame_index, self._emotion))

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
            self._ms_until_blink = self._random_blink_interval()
            self._ms_until_wave = _WAVE_INTERVAL_MS

    def _active_idle_loop(self) -> tuple[int, int]:
        """Return the `(start_index, frame_count)` idle loop the current
        displayed emotion drives: breathing by default, or that emotion's
        own bounce/steam/jitter loop (see `emotion_poses.IDLE_LOOP_FOR_EMOTION`).
        """
        displayed = map_emotion_to_avatar(self._emotion) if self._emotion is not None else None
        loop = IDLE_LOOP_FOR_EMOTION.get(displayed) if displayed is not None else None
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
        self._ms_until_blink -= elapsed_ms
        self._ms_until_wave -= elapsed_ms
        if self._ms_until_blink <= 0:
            self._ms_until_blink = self._random_blink_interval()
            self._start_event(IDLE_BLINK_INDEX, 1)
        elif self._ms_until_wave <= 0:
            self._ms_until_wave = _WAVE_INTERVAL_MS
            self._start_event(IDLE_WAVE_START_INDEX, IDLE_WAVE_FRAME_COUNT)
        else:
            start, count = self._active_idle_loop()
            self._frame_index = start + (self._frame_index - start + 1) % count

    def _start_event(self, start_index: int, frame_count: int) -> None:
        """Begin playing `frame_count` frames starting at `start_index`."""
        self._playing_event = True
        self._event_indices = list(range(start_index + 1, start_index + frame_count))
        self._frame_index = start_index

    def _random_blink_interval(self) -> float:
        """Pick the next blink's delay, uniformly within the spec's 4-7s range."""
        return random.uniform(*_BLINK_INTERVAL_RANGE_MS)
