"""Tracks the countdowns for idle's two randomly/periodically spliced-in
events (a blink, a flipper wave), split out of `animator.py` so it stays
within the project's file-size limit and so the animator's state machine
does not also have to own blink/wave timing arithmetic.
"""

import random

_BLINK_INTERVAL_RANGE_MS = (4000, 7000)
_WAVE_INTERVAL_MS = 12000

BLINK_EVENT = "blink"
WAVE_EVENT = "wave"


class IdleTimers:
    """Two independent countdowns, ticked together each idle frame."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        """Restart both countdowns (on entering idle, or after an event)."""
        self._ms_until_blink = random.uniform(*_BLINK_INTERVAL_RANGE_MS)
        self._ms_until_wave = _WAVE_INTERVAL_MS

    def tick(self, elapsed_ms: int) -> str | None:
        """Advance both countdowns by `elapsed_ms`; return whichever event
        (if any) just became due, resetting only that one's countdown."""
        self._ms_until_blink -= elapsed_ms
        self._ms_until_wave -= elapsed_ms
        if self._ms_until_blink <= 0:
            self._ms_until_blink = random.uniform(*_BLINK_INTERVAL_RANGE_MS)
            return BLINK_EVENT
        if self._ms_until_wave <= 0:
            self._ms_until_wave = _WAVE_INTERVAL_MS
            return WAVE_EVENT
        return None
