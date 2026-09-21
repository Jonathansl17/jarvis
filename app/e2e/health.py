"""Measures whether the Tk main thread stays responsive while the app works.

Three signals, all cheap enough to leave on for a whole run:
- heartbeat: an `after` timer; a gap longer than `stall_seconds` is a stall
  (the main thread was busy or blocked) and its Python stack is recorded;
- idle probe: an `after_idle` callback; Tk repaints from the idle queue, so
  if this stops firing the window has stopped painting even if timers run;
- message counts: camera samples and assistant replies crossing the bridge.
"""

import sys
import threading
import time
import traceback
from collections.abc import Callable
from dataclasses import dataclass, field

from app.ui.bridge import DispatchQueue
from app.ui.messages import AssistantReplied, CameraSampleReady, UiMessage

Schedule = Callable[[int, Callable[[], None]], object]
_HEARTBEAT_MS = 100
_IDLE_PROBE_MS = 50
_WATCHDOG_POLL_SECONDS = 0.1


@dataclass
class Stall:
    """One main-thread stall: how long, and what it was running."""

    seconds: float
    stack: str


@dataclass
class HealthSnapshot:
    """Counters accumulated since the previous snapshot."""

    camera_samples: int = 0
    replies: int = 0
    idle_ticks: int = 0
    stalls: list[Stall] = field(default_factory=list)


class CountingDispatchQueue(DispatchQueue):
    """A `DispatchQueue` that also tallies camera samples and replies."""

    def __init__(self) -> None:
        super().__init__()
        self.camera_samples = 0
        self.replies = 0

    def put(self, message: UiMessage) -> None:
        if isinstance(message, CameraSampleReady):
            self.camera_samples += 1
        elif isinstance(message, AssistantReplied):
            self.replies += 1
        super().put(message)


class HealthMonitor:
    """Runs the heartbeat, the idle probe and a watchdog thread; call `start()`
    from the Tk main thread once the window exists."""

    def __init__(self, schedule: Schedule, schedule_idle: Callable[[Callable[[], None]], object],
                 dispatch: CountingDispatchQueue, stall_seconds: float) -> None:
        self._schedule = schedule
        self._schedule_idle = schedule_idle
        self._dispatch = dispatch
        self._stall_seconds = stall_seconds
        self._main_ident = threading.get_ident()
        self._last_beat = time.monotonic()
        self._idle_ticks = 0
        self._stalls: list[Stall] = []
        self._reported = HealthSnapshot()

    def start(self) -> None:
        """Arm the heartbeat, the idle probe and the watchdog."""
        self._last_beat = time.monotonic()
        self._beat()
        self._schedule_idle(self._idle_tick)
        threading.Thread(target=self._watchdog, daemon=True, name="e2e-watchdog").start()

    def snapshot(self) -> HealthSnapshot:
        """Return the counters since the previous snapshot and reset them."""
        previous, totals = self._reported, HealthSnapshot(
            self._dispatch.camera_samples, self._dispatch.replies, self._idle_ticks, list(self._stalls)
        )
        self._reported = totals
        return HealthSnapshot(
            camera_samples=totals.camera_samples - previous.camera_samples,
            replies=totals.replies - previous.replies,
            idle_ticks=totals.idle_ticks - previous.idle_ticks,
            stalls=totals.stalls[len(previous.stalls):],
        )

    def _beat(self) -> None:
        self._last_beat = time.monotonic()
        self._schedule(_HEARTBEAT_MS, self._beat)

    def _idle_tick(self) -> None:
        self._idle_ticks += 1
        self._schedule(_IDLE_PROBE_MS, lambda: self._schedule_idle(self._idle_tick))

    def _watchdog(self) -> None:
        """Poll the heartbeat; on a stall, capture the main thread's stack once."""
        while True:
            time.sleep(_WATCHDOG_POLL_SECONDS)
            silent_for = time.monotonic() - self._last_beat
            if silent_for < self._stall_seconds:
                continue
            frame = sys._current_frames().get(self._main_ident)
            stack = "".join(traceback.format_stack(frame)) if frame is not None else ""
            self._stalls.append(Stall(silent_for, stack))
            while time.monotonic() - self._last_beat >= self._stall_seconds:
                time.sleep(_WATCHDOG_POLL_SECONDS)
