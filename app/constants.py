"""Named values fixed across environments: env var names, wire-level routes,
the wake word, and the default Gemini model.

Anything that varies per deployment lives in `config.py` instead.
"""

GEMINI_API_KEY_ENV_VAR = "GEMINI_API_KEY"
API_BASE_URL_ENV_VAR = "API_BASE_URL"

DEFAULT_API_BASE_URL = "http://localhost:8000"
DEFAULT_GEMINI_MODEL = "gemini-3.6-flash"

PREDICT_ROUTE_PREFIX = "/predict"
MODELS_ROUTE = "/models"
HEALTH_ROUTE = "/health"
OPENAPI_ROUTE = "/openapi.json"

# Matched case-insensitively against the start of an utterance; the longer
# two-word form must be checked before the compact form is assumed absent.
WAKE_WORDS = ("jarvistec", "jarvis tec")

MODELS_DIR_ENV_VAR = "MODELS_DIR"
PIPER_CACHE_DIR_ENV_VAR = "PIPER_CACHE_DIR"

FACIAL_EMOTION_MODEL_FILENAME = "facial_emotion_cnn.onnx"
FACE_CASCADE_FILENAME = "haarcascade_frontalface_alt.xml"

# Order fixed to match the ONNX model's softmax output; never reorder.
EMOTION_LABELS = ("angry", "disgust", "fear", "happy", "sad", "surprise", "neutral")
EMOTION_INPUT_SIZE_PX = 48
FACE_CASCADE_SCALE_FACTOR = 1.32
FACE_CASCADE_MIN_NEIGHBORS = 5
CAMERA_INDEX = 0
EMOTION_SAMPLE_INTERVAL_SECONDS = 5.0

STT_SAMPLE_RATE_HZ = 16000
WHISPER_MODEL_SIZE = "small"
WHISPER_LANGUAGE = "es"
WHISPER_DEVICE = "cpu"

PIPER_VOICE_NAME = "es_MX-claude-high"
PIPER_MODEL_FILE_SUFFIX = ".onnx"
PIPER_CONFIG_FILE_SUFFIX = ".onnx.json"
PIPER_SAMPLE_RATE_HZ = 22050
