"""Composition root: builds every concrete adapter and returns a ready `App`.

The only file allowed to import both a Protocol and its concrete
implementation together (see `app-architecture.md`'s dependency direction).
"""

from typing import Any

from app.api_client.http_client import HttpPredictionClient
from app.api_client.protocol import PredictionClient
from app.config import Settings, get_settings
from app.constants import (
    CAMERA_FRAME_INTERVAL_SECONDS,
    CAMERA_INDEX,
    EMOTION_SAMPLE_INTERVAL_SECONDS,
    FACE_CASCADE_FILENAME,
    FACIAL_EMOTION_MODEL_FILENAME,
    WHISPER_DEVICE,
    WHISPER_LANGUAGE,
    WHISPER_MODEL_SIZE,
)
from app.conversation import Conversation
from app.dialogue.orchestrator import DialogueOrchestrator
from app.emotion.camera import Camera
from app.emotion.face_locator import FaceLocator
from app.emotion.onnx_backend import OnnxEmotionDetector
from app.emotion.tone_adapter import ToneAdapter
from app.errors import PredictionRequestError
from app.intents.composite_parser import CompositeIntentParser
from app.intents.gemini_parser import GeminiParser
from app.intents.parser import IntentParser
from app.intents.rules.rules_parser import RulesParser
from app.speech.stt.recorder import AudioRecorder
from app.speech.stt.whisper_backend import WhisperSpeechToText
from app.speech.tts.piper_backend import PiperTextToSpeech
from app.speech.tts.player import AudioPlayer
from app.speech.tts.voice_cache import ensure_voice_downloaded
from app.ui.collaborators import (
    AppCollaborators,
    DialogueCollaborators,
    EmotionCollaborators,
    RuntimeOptions,
    SpeechCollaborators,
)
from app.ui.strings import STATUS_IA_RULES

_STT_ENGINE_NAME_TEMPLATE = "whisper-{model_size}"


async def create_app() -> AppCollaborators:
    """Wire every non-UI adapter together, ready for `JarvisApp`'s constructor.

    Async because building the intent parser fetches model schemas over
    HTTP; the `httpx.AsyncClient` it shares with the rest of the app's
    lifetime must be used from a single event loop throughout, so this
    coroutine must be submitted onto the bridge's background loop (see
    `__main__.py`), never run behind its own throwaway `asyncio.run()`.

    Returns collaborators rather than a constructed `JarvisApp`: building
    the Tk root must happen on the main thread, not this background loop's
    thread, which is why `__main__.py` constructs `JarvisApp` itself.
    """
    settings = get_settings()
    prediction_client = HttpPredictionClient(settings.api_base_url)
    intent_parser = await _build_intent_parser(settings, prediction_client)
    conversation = Conversation()
    orchestrator = DialogueOrchestrator(
        intent_parser, prediction_client, ToneAdapter(), conversation
    )
    return AppCollaborators(
        dialogue=DialogueCollaborators(orchestrator, prediction_client, conversation),
        speech=_build_speech(settings),
        emotion=_build_emotion(settings),
        options=RuntimeOptions(
            stt_engine_name=_STT_ENGINE_NAME_TEMPLATE.format(model_size=WHISPER_MODEL_SIZE),
            camera_enabled=settings.camera_enabled,
            tts_enabled=settings.tts_enabled,
            camera_frame_interval_seconds=CAMERA_FRAME_INTERVAL_SECONDS,
            emotion_interval_seconds=EMOTION_SAMPLE_INTERVAL_SECONDS,
            initial_ia_state=_initial_ia_state(intent_parser, settings),
        ),
    )


async def _build_intent_parser(settings: Settings, prediction_client: PredictionClient) -> IntentParser:
    """Build the Gemini+rules composite, or rules alone if either is unavailable."""
    rules_parser = RulesParser()
    if not settings.gemini_api_key:
        return rules_parser
    try:
        schemas = await _fetch_model_schemas(prediction_client)
    except PredictionRequestError:
        return rules_parser
    gemini_parser = GeminiParser(settings.gemini_api_key, settings.gemini_models, schemas)
    return CompositeIntentParser(gemini_parser, rules_parser)


def _initial_ia_state(intent_parser: IntentParser, settings: Settings) -> str:
    """Return the status strip's starting IA label: the first Gemini model, or "reglas"."""
    if isinstance(intent_parser, CompositeIntentParser):
        return settings.gemini_models[0]
    return STATUS_IA_RULES


async def _fetch_model_schemas(prediction_client: PredictionClient) -> dict[str, Any]:
    """Fetch every model's request schema, keyed by model name."""
    model_names = await prediction_client.list_models()
    return {name: await prediction_client.model_schema(name) for name in model_names}


def _build_speech(settings: Settings) -> SpeechCollaborators:
    """Build the recorder/STT/TTS/player quartet, downloading the voice once."""
    voice_path = ensure_voice_downloaded(settings.piper_cache_dir)
    return SpeechCollaborators(
        recorder=AudioRecorder(),
        stt=WhisperSpeechToText(WHISPER_MODEL_SIZE, WHISPER_LANGUAGE, WHISPER_DEVICE),
        tts=PiperTextToSpeech(voice_path),
        player=AudioPlayer(),
    )


def _build_emotion(settings: Settings) -> EmotionCollaborators:
    """Build the camera and its ONNX-backed face/emotion detector."""
    face_locator = FaceLocator(settings.models_dir / FACE_CASCADE_FILENAME)
    detector = OnnxEmotionDetector(settings.models_dir / FACIAL_EMOTION_MODEL_FILENAME, face_locator)
    return EmotionCollaborators(camera=Camera(CAMERA_INDEX), detector=detector)
