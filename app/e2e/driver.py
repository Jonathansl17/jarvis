"""Drives the real window through one turn per model and judges the run.

Each turn presses the mic, holds it, and releases it with the sentence
queued on the scripted recorder (so whisper transcribes real speech).
Between turns the health monitor's counters are logged; at the end the run
passes only if every turn was answered and the main thread never stalled
after startup.
"""

import time
from collections.abc import Callable
from dataclasses import dataclass

from app.e2e.health import HealthMonitor, HealthSnapshot
from app.e2e.prompts import ModelPrompt
from app.e2e.speech_injection import ScriptedSpeechRecorder
from app.ui.app import JarvisApp

_TIMESTAMP_FORMAT = "%H:%M:%S"
_TURN_LINE = "[{time}] turn {index}/{total} {model}: camera={camera}/s idle={idle}/s replies={replies} stalls={stalls}"
_STALL_LINE = "  stall {seconds:.1f}s on the main thread:\n{stack}"
_VERDICT_LINE = "{verdict}: {answered}/{total} turns answered, {stalls} main-thread stall(s) after startup"
_PASS, _FAIL = "PASS", "FAIL"
_MILLISECONDS = 1000


@dataclass(frozen=True)
class DriverTiming:
    """Seconds between turns, and how long the mic is held in voice mode."""

    turn_interval_seconds: float
    mic_hold_seconds: float


class SmokeDriver:
    """Schedules the turns on Tk's timer and writes the report through `log`."""

    def __init__(self, app: JarvisApp, monitor: HealthMonitor, timing: DriverTiming,
                 log: Callable[[str], None]) -> None:
        self._app = app
        self._monitor = monitor
        self._timing = timing
        self._log = log
        self._prompts: list[ModelPrompt] = []
        self._recorder: ScriptedSpeechRecorder | None = None  # Set by `run()`.
        self._index = 0
        self._answered = 0
        self._stalls = 0
        self.passed = False

    def run(self, prompts: list[ModelPrompt], recorder: ScriptedSpeechRecorder,
            startup_delay_seconds: float) -> None:
        """Start the monitor and the first turn once the window has settled."""
        self._prompts = prompts
        self._recorder = recorder
        self._monitor.start()
        self._app.root.after(int(startup_delay_seconds * _MILLISECONDS), self._begin_turn)

    def _begin_turn(self) -> None:
        """Log the previous turn's health, then submit the next sentence or finish."""
        health = self._monitor.snapshot()
        if self._index > 0:  # The first snapshot is startup noise: camera opening, model loading.
            self._report_turn(health)
        if self._index >= len(self._prompts):
            self._finish()
            return
        self._press_mic_and_speak(self._prompts[self._index].text)
        self._index += 1
        self._app.root.after(int(self._timing.turn_interval_seconds * _MILLISECONDS), self._begin_turn)

    def _report_turn(self, health: HealthSnapshot) -> None:
        interval = self._timing.turn_interval_seconds
        prompt = self._prompts[self._index - 1]
        self._answered += min(health.replies, 1)
        self._stalls += len(health.stalls)
        self._log(_TURN_LINE.format(
            time=time.strftime(_TIMESTAMP_FORMAT), index=self._index, total=len(self._prompts),
            model=prompt.model_title, camera=round(health.camera_samples / interval),
            idle=round(health.idle_ticks / interval), replies=health.replies, stalls=len(health.stalls),
        ))
        for stall in health.stalls:
            self._log(_STALL_LINE.format(seconds=stall.seconds, stack=stall.stack))

    def _press_mic_and_speak(self, text: str) -> None:
        assert self._recorder is not None
        self._recorder.say_next(text)
        self._app.on_mic_toggle()
        self._app.root.after(int(self._timing.mic_hold_seconds * _MILLISECONDS), self._app.on_mic_toggle)

    def _finish(self) -> None:
        total = len(self._prompts)
        self.passed = self._answered == total and self._stalls == 0
        self._log(_VERDICT_LINE.format(
            verdict=_PASS if self.passed else _FAIL, answered=self._answered, total=total, stalls=self._stalls
        ))
        self._app.on_quit()
