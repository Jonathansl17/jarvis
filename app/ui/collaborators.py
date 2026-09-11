"""Parameter-object bundles for `JarvisApp`'s constructor.

`JarvisApp` composes roughly a dozen collaborators; grouping them by concern
keeps its constructor within the project's 4-parameter ceiling.
"""

from collections.abc import Sequence
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
    """Startup flags and text that do not belong to a single collaborator."""

    stt_engine_name: str
    camera_enabled: bool
    tts_enabled: bool
    preview_interval_seconds: float
    emotion_interval_seconds: float
    startup_notices: Sequence[str] = ()
