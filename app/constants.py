"""Named values fixed across environments: env var names, wire-level routes,
the wake word, and the default Gemini model.

Anything that varies per deployment lives in `config.py` instead.
"""

GEMINI_API_KEY_ENV_VAR = "GEMINI_API_KEY"
GEMINI_MODELS_ENV_VAR = "GEMINI_MODELS"
API_BASE_URL_ENV_VAR = "API_BASE_URL"

DEFAULT_API_BASE_URL = "http://localhost:8000"
# Tried in order; `GeminiParser` moves to the next model on a quota error
# (429) or a retired model (404), so a free-tier daily limit on the first
# model does not stop the assistant from using Gemini at all that day.
GEMINI_MODEL_CHAIN = ("gemini-3.6-flash", "gemini-flash-lite-latest")

PREDICT_ROUTE_PREFIX = "/predict"
MODELS_ROUTE = "/models"
MODEL_SCHEMA_ROUTE_TEMPLATE = MODELS_ROUTE + "/{model_name}/schema"
HEALTH_ROUTE = "/health"
OPENAPI_ROUTE = "/openapi.json"

# Matched case-insensitively against the start of an utterance. Includes the
# STT mishearings observed in practice ("yarvis", "yalvis", "jarvi"); each
# entry is still checked on a full-word boundary, so ordering does not
# affect which one matches.
WAKE_WORDS = (
    "jarvistec", "jarvis tec", "yalvis tec", "yarvis tec",
    "jarvis", "yarvis", "yalvis", "jarvi",
)

MODELS_DIR_ENV_VAR = "MODELS_DIR"
PIPER_CACHE_DIR_ENV_VAR = "PIPER_CACHE_DIR"
CAMERA_ENABLED_ENV_VAR = "CAMERA_ENABLED"
TTS_ENABLED_ENV_VAR = "TTS_ENABLED"

FACIAL_EMOTION_MODEL_FILENAME = "facial_emotion_cnn.onnx"
FACE_CASCADE_FILENAME = "haarcascade_frontalface_alt.xml"

# Order fixed to match the ONNX model's softmax output; never reorder.
EMOTION_LABELS = ("angry", "disgust", "fear", "happy", "sad", "surprise", "neutral")
EMOTION_INPUT_SIZE_PX = 48
FACE_SCALE_FACTOR = 1.1
FACE_MIN_NEIGHBORS = 4
# Rejects tiny false positives (screen glare, texture patches); in pixels,
# before the frame is scaled to the preview grid.
FACE_MIN_SIZE = (60, 60)
CAMERA_INDEX = 0
# A freshly opened USB webcam's first frames are near-black while its auto
# exposure settles; discarding a few on open avoids reporting "no face"
# during that warm-up window.
CAMERA_WARMUP_FRAMES = 10
# How often the camera worker thread grabs a new frame (~15 fps); the
# emotion detector runs far less often (`EMOTION_SAMPLE_INTERVAL_SECONDS`),
# reusing its last result on the frames in between so the face box stays
# drawn live.
CAMERA_FRAME_INTERVAL_SECONDS = 1 / 15
# Threads each ONNX session (speech and emotion) may use, so inference never
# starves the interface thread on a shared CPU.
ONNX_INTRA_OP_THREADS = 2
EMOTION_SAMPLE_INTERVAL_SECONDS = 2.0
# The winning emotion always drives the avatar and the tone: with seven
# classes a webcam reading rarely exceeds 50 percent, so the confidence is
# shown for information only.

STT_SAMPLE_RATE_HZ = 16000
WHISPER_MODEL_SIZE = "small"
WHISPER_LANGUAGE = "es"
WHISPER_DEVICE = "cpu"
# int8 runs faster on CPU and avoids the float16 conversion warning
WHISPER_COMPUTE_TYPE = "int8"

PIPER_VOICE_NAME = "es_MX-claude-high"
PIPER_MODEL_FILE_SUFFIX = ".onnx"
PIPER_CONFIG_FILE_SUFFIX = ".onnx.json"
PIPER_SAMPLE_RATE_HZ = 22050
