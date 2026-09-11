"""Domain error types raised across the app, one per failure boundary.

Every subclass preserves the triggering exception via `from exc` at the
raise site; this module only defines the vocabulary, it never raises.
"""


class AppError(Exception):
    """Base class for every domain error the app can raise."""


class SpeechRecognitionError(AppError):
    """Raised when recording or transcribing microphone audio fails."""


class SynthesisError(AppError):
    """Raised when synthesizing or playing back speech fails."""


class EmotionDetectionError(AppError):
    """Raised when reading the webcam or classifying a face fails."""


class IntentParsingError(AppError):
    """Raised when neither the rules parser nor Gemini can resolve an intent."""


class PredictionRequestError(AppError):
    """Raised when calling the prediction REST API fails."""
