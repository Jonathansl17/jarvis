"""Composes the JarvisTEC screen; behavior lives in `ui/actions.py`."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import Input

from app.dialogue.strings import GREETING_TEXT
from app.ui.actions import JarvisActions
from app.ui.collaborators import (
    DialogueCollaborators,
    EmotionCollaborators,
    RuntimeOptions,
    SpeechCollaborators,
)
from app.ui.widgets.avatar_pane import AvatarPane
from app.ui.widgets.conversation_log import ConversationLog
from app.ui.widgets.status_bar import StatusBar

_INPUT_PLACEHOLDER = "Escribe y presiona Enter, o con la caja vacía presiona espacio para hablar…"
_KEY_BINDING_RECORD = "hablar"
_KEY_BINDING_CAMERA = "cámara"
_KEY_BINDING_QUIT = "salir"
_KEY_RECORD = "space"
_KEY_CAMERA = "ctrl+e"
_KEY_QUIT = "ctrl+q"


class JarvisApp(JarvisActions, App):
    """The TUI: avatar pane, conversation log, input line, and status bar."""

    CSS_PATH = "styles.tcss"
    # priority=True so the keys work while the input line has focus. Space
    # only records when the input is empty, otherwise it types a space.
    BINDINGS = [
        Binding(_KEY_RECORD, "toggle_recording", _KEY_BINDING_RECORD, priority=True),
        Binding(_KEY_CAMERA, "toggle_camera", _KEY_BINDING_CAMERA, priority=True),
        Binding(_KEY_QUIT, "quit", _KEY_BINDING_QUIT, priority=True),
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
            yield AvatarPane(id="avatar")
            yield ConversationLog(id="log")
        yield Input(placeholder=_INPUT_PLACEHOLDER, id="input-line")
        yield StatusBar(self._stt_engine_name, id="status-bar")

    def on_mount(self) -> None:
        """Greet the user, surface any startup notices, and start the camera."""
        log = self.query_one(ConversationLog)
        log.append_turn("assistant", GREETING_TEXT)
        for notice in self._startup_notices:
            log.append_turn("system", notice)
        self.query_one("#input-line").focus()
        if self._camera_enabled:
            self._start_emotion_worker()

    def on_unmount(self) -> None:
        """Release the webcam device on shutdown."""
        self._camera.close()
