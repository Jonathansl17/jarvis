"""Composes the JarvisTEC screen; behavior lives in `ui/actions.py`."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Input

from app.dialogue.strings import GREETING_TEXT
from app.intents.models import Speaker
from app.ui.actions import JarvisActions
from app.ui.collaborators import (
    DialogueCollaborators,
    EmotionCollaborators,
    RuntimeOptions,
    SpeechCollaborators,
)
from app.ui.key_bindings import KEY_BINDINGS
from app.ui.widgets.avatar_pane import AvatarPane
from app.ui.widgets.camera_preview import CameraPreview
from app.ui.widgets.conversation_log import ConversationLog
from app.ui.widgets.status_bar import StatusBar

_INPUT_PLACEHOLDER = "Escribe y presiona Enter, o Ctrl+Espacio (o Ctrl+T) para hablar…"


class JarvisApp(JarvisActions, App):
    """The TUI: avatar pane, conversation log, input line, and status bar."""

    CSS_PATH = "styles.tcss"
    # priority=True so the keys work while the input line has focus.
    BINDINGS = [
        Binding(
            spec.key,
            spec.action,
            spec.description,
            priority=True,
            key_display=spec.key_display,
        )
        for spec in KEY_BINDINGS
    ]

    def __init__(
        self,
        *,
        dialogue: DialogueCollaborators,
        speech: SpeechCollaborators,
        emotion: EmotionCollaborators,
        options: RuntimeOptions,
    ) -> None:
        super().__init__()
        self._orchestrator = dialogue.orchestrator
        self._prediction_client = dialogue.prediction_client
        self._conversation = dialogue.conversation
        self._recorder = speech.recorder
        self._stt = speech.stt
        self._tts = speech.tts
        self._player = speech.player
        self._camera = emotion.camera
        self._emotion_detector = emotion.detector
        self._stt_engine_name = options.stt_engine_name
        self._camera_enabled = options.camera_enabled
        self._tts_enabled = options.tts_enabled
        self._emotion_interval_seconds = options.emotion_interval_seconds
        self._startup_notices = options.startup_notices
        self._recording = False

    def compose(self) -> ComposeResult:
        with Horizontal(id="top-region"):
            with Vertical(id="left-pane"):
                yield AvatarPane(id="avatar")
                yield CameraPreview(id="camera-preview")
            yield ConversationLog(id="log")
        yield Input(placeholder=_INPUT_PLACEHOLDER, id="input-line")
        yield StatusBar(self._stt_engine_name, id="status-bar")

    def on_mount(self) -> None:
        """Greet the user, surface any startup notices, and start the camera."""
        log = self.query_one(ConversationLog)
        log.append_turn(Speaker.ASSISTANT, GREETING_TEXT)
        for notice in self._startup_notices:
            log.append_turn(Speaker.SYSTEM, notice)
        self.query_one("#input-line").focus()
        if self._camera_enabled:
            self._start_emotion_worker()

    def on_unmount(self) -> None:
        """Release the webcam device on shutdown."""
        self._camera.close()
