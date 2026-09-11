"""Parameter-object bundles for `JarvisApp`'s constructor.

`JarvisApp` composes roughly a dozen collaborators; grouping them by concern
keeps its constructor within the project's 4-parameter ceiling.
"""

from dataclasses import dataclass

from app.api_client.protocol import PredictionClient
from app.conversation import Conversation
from app.dialogue.orchestrator import DialogueOrchestrator
from app.emotion.camera import Camera
from app.emotion.protocol import EmotionDetector
from app.speech.stt.protocol import SpeechToText
from app.speech.stt.recorder import AudioRecorder
from app.speech.tts.player import AudioPlayer
from app.speech.tts.protocol import TextToSpeech
from app.ui.bridge import DispatchQueue, EventLoopThread


@dataclass(frozen=True)
class DialogueCollaborators:
    """Everything `JarvisApp` needs to run one dialogue turn."""

    orchestrator: DialogueOrchestrator
    prediction_client: PredictionClient
    conversation: Conversation


@dataclass(frozen=True)
class SpeechCollaborators:
    """Everything `JarvisApp` needs for push-to-talk and text-to-speech."""

    recorder: AudioRecorder
    stt: SpeechToText
    tts: TextToSpeech
    player: AudioPlayer


@dataclass(frozen=True)
class EmotionCollaborators:
    """Everything `JarvisApp` needs to sample and classify the webcam."""

    camera: Camera
    detector: EmotionDetector


@dataclass(frozen=True)
class RuntimeOptions:
    """Startup flags and text that do not belong to a single collaborator.

    `initial_ia_state` seeds the status strip's IA field (a Gemini model
    name, or "reglas"); system notices about the intent parser surface
    there, never as a chat line — see `ui/notice_parsing.py`.
    """

    stt_engine_name: str
    camera_enabled: bool
    tts_enabled: bool
    camera_frame_interval_seconds: float
    emotion_interval_seconds: float
    initial_ia_state: str


@dataclass(frozen=True)
class RuntimeCollaborators:
    """The sync/async bridge and its runtime flags, bundled for `JarvisApp`."""

    bridge: EventLoopThread
    dispatch: DispatchQueue
    options: RuntimeOptions


@dataclass(frozen=True)
class AppCollaborators:
    """Every non-UI collaborator `create_app()` builds, before `JarvisApp` exists.

    `JarvisApp.__init__` creates the Tk root, so it must run on the main
    thread; `create_app()` runs on the background bridge thread instead
    (the `httpx.AsyncClient` it builds must be used from that same loop for
    the app's lifetime). Splitting the two keeps Tk's window creation and
    its `mainloop()` on the same thread, which Tk requires.
    """

    dialogue: DialogueCollaborators
    speech: SpeechCollaborators
    emotion: EmotionCollaborators
    options: RuntimeOptions
