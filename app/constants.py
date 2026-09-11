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
