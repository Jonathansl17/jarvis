"""Entry point for `python -m app`, run from the repository root.

Synchronous by design: Tk's `root.mainloop()` must own the main thread. The
background bridge loop runs `create_app()` (and everything else async) for
the app's whole lifetime, never a throwaway `asyncio.run()` on this thread;
`JarvisApp` itself — which creates the Tk root — is built here, on the main
thread, since Tk requires its window and its `mainloop()` on the same one.
"""

from app.main import create_app
from app.ui.app import JarvisApp
from app.ui.bridge import DispatchQueue, EventLoopThread
from app.ui.collaborators import RuntimeCollaborators


def main() -> None:
    """Start the bridge, build the collaborators on it, then run the Tk app."""
    bridge = EventLoopThread()
    bridge.start()
    dispatch = DispatchQueue()
    collaborators = bridge.submit(create_app()).result()
    app = JarvisApp(
        dialogue=collaborators.dialogue,
        speech=collaborators.speech,
        emotion=collaborators.emotion,
        runtime=RuntimeCollaborators(bridge=bridge, dispatch=dispatch, options=collaborators.options),
    )
    app.run()


if __name__ == "__main__":
    main()
