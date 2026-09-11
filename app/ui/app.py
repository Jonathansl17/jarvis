"""Composes the JarvisTEC desktop window; behavior lives in `ui/actions.py`
and `ui/dispatch_handlers.py`, layout in `ui/layout.py`."""

import customtkinter as ctk

from app.dialogue.strings import GREETING_TEXT
from app.intents.models import Speaker
from app.ui import layout, theme
from app.ui.actions import JarvisActions
from app.ui.collaborators import (
    DialogueCollaborators,
    EmotionCollaborators,
    RuntimeCollaborators,
    SpeechCollaborators,
)
from app.ui.dispatch_handlers import JarvisDispatchHandlers
from app.ui.key_bindings import KEY_BINDINGS
from app.ui.layout_types import StatusBarInfo, WindowCallbacks

_DISPATCH_POLL_MS = 50


class JarvisApp(JarvisActions, JarvisDispatchHandlers):
    """The desktop GUI: avatar/camera cards, conversation, input, status strip."""

    def __init__(
        self,
        *,
        dialogue: DialogueCollaborators,
        speech: SpeechCollaborators,
        emotion: EmotionCollaborators,
        runtime: RuntimeCollaborators,
    ) -> None:
        self._orchestrator = dialogue.orchestrator
        self._conversation = dialogue.conversation
        self._recorder, self._stt = speech.recorder, speech.stt
        self._tts, self._player = speech.tts, speech.player
        self._camera, self._emotion_detector = emotion.camera, emotion.detector
        self._bridge, self._dispatch = runtime.bridge, runtime.dispatch
        options = runtime.options
        self._tts_enabled = options.tts_enabled
        self._camera_enabled = options.camera_enabled
        self._camera_frame_interval_seconds = options.camera_frame_interval_seconds
        self._emotion_interval_seconds = options.emotion_interval_seconds
        self._recording = False
        self._camera_worker = None
        self.root = ctk.CTk()
        self._build_window(options.stt_engine_name, options.initial_ia_state)

    def run(self) -> None:
        """Show the greeting, start the camera if enabled, and block on Tk."""
        self.conversation_view.append_turn(Speaker.ASSISTANT, GREETING_TEXT)
        if self._camera_enabled:
            self._start_camera_worker()
        else:
            self.camera_preview.show_disabled()
        self.root.after(_DISPATCH_POLL_MS, self._poll_dispatch)
        self.root.mainloop()

    def destroy_app(self) -> None:
        """Release the webcam and audio client, then close the window."""
        if self._camera_worker is not None:
            self._camera_worker.stop()
        else:
            self._camera.close()
        self._bridge.stop()
        self.root.destroy()

    def _build_window(self, stt_engine_name: str, initial_ia_state: str) -> None:
        """Lay out the window's widgets, bind global keys, and wire the close handler."""
        fonts = theme.apply_theme()
        callbacks = WindowCallbacks(
            on_send=self.on_send, on_mic_toggle=self.on_mic_toggle, on_camera_toggle=self.on_camera_toggle
        )
        widgets = layout.build_window(self.root, fonts, StatusBarInfo(stt_engine_name, initial_ia_state), callbacks)
        self.avatar_pane = widgets.avatar_pane
        self.camera_preview = widgets.camera_preview
        self.camera_toggle_button = widgets.camera_toggle_button
        self.conversation_view = widgets.conversation_view
        self.input_row = widgets.input_row
        self.status_bar = widgets.status_bar

        for spec in KEY_BINDINGS:
            self.root.bind(spec.sequence, lambda _event, action=spec.action: getattr(self, action)())
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)

    def _poll_dispatch(self) -> None:
        """Drain the bridge queue and dispatch each message, then reschedule."""
        for message in self._dispatch.poll():
            self.dispatch(message)
        self.root.after(_DISPATCH_POLL_MS, self._poll_dispatch)
