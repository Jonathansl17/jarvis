"""Composition root: builds every concrete adapter and returns a ready `App`.

The only file allowed to import both a Protocol and its concrete
implementation together (see `app-architecture.md`'s dependency direction).
"""

from typing import Any

from app.api_client.http_client import HttpPredictionClient
from app.api_client.protocol import PredictionClient
from app.config import Settings, get_settings
from app.constants import (
    CAMERA_INDEX,
    DEFAULT_GEMINI_MODEL,
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
from app.ui.app import JarvisApp
from app.ui.collaborators import (
    DialogueCollaborators,
    EmotionCollaborators,
    RuntimeOptions,
    SpeechCollaborators,
)

_STT_ENGINE_NAME_TEMPLATE = "whisper-{model_size}"
_NOTICE_GEMINI_DISABLED = "Gemini no está configurado; usando reglas por palabra clave."
_NOTICE_API_UNREACHABLE = "No se pudo contactar la API para obtener esquemas; usando reglas."


async def create_app() -> JarvisApp:
    """Wire every concrete adapter together and return the ready `JarvisApp`.

    Async because building the intent parser fetches model schemas over
    HTTP; the `httpx.AsyncClient` it shares with the rest of the app's
    lifetime must be used from a single event loop throughout, so this
    coroutine has to run on the same loop the caller later runs the `App`
    on (see `__main__.py`), never behind its own throwaway `asyncio.run()`.
    """
    settings = get_settings()
    prediction_client = HttpPredictionClient(settings.api_base_url)
    startup_notices: list[str] = []
    intent_parser = await _build_intent_parser(settings, prediction_client, startup_notices)
    conversation = Conversation()
    orchestrator = DialogueOrchestrator(
        intent_parser, prediction_client, ToneAdapter(), conversation
    )
    return JarvisApp(
        dialogue=DialogueCollaborators(orchestrator, prediction_client, conversation),
        speech=_build_speech(settings),
        emotion=_build_emotion(settings),
        options=RuntimeOptions(
            stt_engine_name=_STT_ENGINE_NAME_TEMPLATE.format(model_size=WHISPER_MODEL_SIZE),
            camera_enabled=settings.camera_enabled,
            tts_enabled=settings.tts_enabled,
            emotion_interval_seconds=EMOTION_SAMPLE_INTERVAL_SECONDS,
            startup_notices=startup_notices,
        ),
    )


async def _build_intent_parser(
    settings: Settings, prediction_client: PredictionClient, startup_notices: list[str]
) -> IntentParser:
    """Build the Gemini+rules composite, or rules alone, logging why if so."""
    rules_parser = RulesParser()
    if not settings.gemini_api_key:
        startup_notices.append(_NOTICE_GEMINI_DISABLED)
        return rules_parser
    try:
        schemas = await _fetch_model_schemas(prediction_client)
    except PredictionRequestError:
        startup_notices.append(_NOTICE_API_UNREACHABLE)
        return rules_parser
    gemini_parser = GeminiParser(settings.gemini_api_key, DEFAULT_GEMINI_MODEL, schemas)
    return CompositeIntentParser(gemini_parser, rules_parser)


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
