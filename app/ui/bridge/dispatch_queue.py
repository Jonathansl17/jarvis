"""A thread-safe mailbox for background events, drained by Tk's `after`.

Tk widgets must only ever be touched from the main thread. Background
threads and the bridge's event loop thread `put()` messages here; the main
thread `poll()`s the queue on a timer and reacts to whatever it drains.
"""

import queue

from app.ui.messages import UiMessage


class DispatchQueue:
    """Thread-safe mailbox of `UiMessage`s waiting for the Tk main thread."""

    def __init__(self) -> None:
        self._queue: queue.Queue[UiMessage] = queue.Queue()

    def put(self, message: UiMessage) -> None:
        """Enqueue `message`; safe to call from any thread."""
        self._queue.put(message)

    def poll(self) -> list[UiMessage]:
        """Drain and return every message currently queued, without blocking."""
        messages: list[UiMessage] = []
        while True:
            try:
                messages.append(self._queue.get_nowait())
            except queue.Empty:
                return messages
