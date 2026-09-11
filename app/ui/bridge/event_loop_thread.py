"""Owns the background asyncio event loop the GUI's whole lifetime runs on.

Tk's `root.mainloop()` is synchronous and must own the main thread, but
`httpx.AsyncClient` and every coroutine in `dialogue/`, `intents/`,
`api_client/` need one event loop that lives for the app's lifetime. This
class provides that loop on a dedicated background thread, so Tk code can
submit coroutines to it without ever running one on the main thread itself.
"""

import asyncio
import concurrent.futures
import threading
from collections.abc import Coroutine
from typing import Any, TypeVar

T = TypeVar("T")


class EventLoopThread:
    """Runs one asyncio event loop on a dedicated thread until `stop()`."""

    def __init__(self) -> None:
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._ready = threading.Event()

    def start(self) -> None:
        """Start the background thread and block until its loop is running."""
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        self._ready.wait()

    def submit(self, coro: Coroutine[Any, Any, T]) -> concurrent.futures.Future[T]:
        """Schedule `coro` on the background loop; returns immediately."""
        if self._loop is None:
            raise RuntimeError("EventLoopThread.submit() called before start()")
        return asyncio.run_coroutine_threadsafe(coro, self._loop)

    def stop(self) -> None:
        """Stop the background loop and join its thread."""
        if self._loop is not None:
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread is not None:
            self._thread.join()

    def _run(self) -> None:
        """Create the loop on this thread, signal readiness, then run it."""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._ready.set()
        self._loop.run_forever()
        self._loop.close()
