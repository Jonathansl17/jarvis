"""Renders the fixed-order status line (§6 of the design spec)."""

from textual.widgets import Static

from app.constants import EMOTION_LOW_CONFIDENCE_THRESHOLD
from app.ui.key_bindings import KEY_BINDINGS

FIELD_SEPARATOR = "  │  "
_KEY_HINT_TEMPLATE = "{key}:{description}"
_KEY_HINT_SEPARATOR = "  "
KEY_HINTS_TEXT = _KEY_HINT_SEPARATOR.join(
    _KEY_HINT_TEMPLATE.format(key=spec.key_display or spec.key, description=spec.description)
    for spec in KEY_BINDINGS
)

MIC_LISTO = "LISTO"
MIC_GRABANDO = "GRABANDO"
MIC_PROCESANDO = "PROCESANDO"

EMO_UNCERTAIN = "incierto"
EMO_DISABLED = "desactivado"

API_OK = "OK"
API_SLOW = "LENTO"
API_DOWN = "CAÍDA"

_STT_FIELD_TEMPLATE = "STT:{engine}"
_MIC_FIELD_TEMPLATE = "MIC:{state}"
_EMO_FIELD_TEMPLATE = "EMO:{label} {confidence:.2f}"
_EMO_FIELD_NO_CONFIDENCE_TEMPLATE = "EMO:{label}"
_API_FIELD_TEMPLATE = "API:{state}"


class StatusBar(Static):
    """Shows MIC/EMO/API/STT state and the fixed key hints, in that order."""

    def __init__(self, stt_engine_name: str, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._stt_engine_name = stt_engine_name
        self._mic_state = MIC_LISTO
        self._emo_field = _EMO_FIELD_NO_CONFIDENCE_TEMPLATE.format(label=EMO_DISABLED)
        self._api_state = API_OK

    def on_mount(self) -> None:
        self._refresh_display()

    def set_mic_state(self, state: str) -> None:
        """Update the MIC field to `state` (LISTO, GRABANDO, or PROCESANDO)."""
        self._mic_state = state
        self._refresh_display()

    def set_emotion(self, label: str | None, confidence: float | None) -> None:
        """Update the EMO field, showing `incierto` below the confidence cutoff."""
        if label is None:
            self._emo_field = _EMO_FIELD_NO_CONFIDENCE_TEMPLATE.format(label=EMO_DISABLED)
        elif confidence is not None and confidence < EMOTION_LOW_CONFIDENCE_THRESHOLD:
            self._emo_field = _EMO_FIELD_NO_CONFIDENCE_TEMPLATE.format(label=EMO_UNCERTAIN)
        else:
            self._emo_field = _EMO_FIELD_TEMPLATE.format(label=label, confidence=confidence)
        self._refresh_display()

    def set_api_state(self, state: str) -> None:
        """Update the API field to `state` (OK, LENTO, or CAÍDA)."""
        self._api_state = state
        self._refresh_display()

    def _refresh_display(self) -> None:
        """Recompose the fixed-order field list and update the displayed text."""
        fields = [
            _MIC_FIELD_TEMPLATE.format(state=self._mic_state),
            self._emo_field,
            _API_FIELD_TEMPLATE.format(state=self._api_state),
            _STT_FIELD_TEMPLATE.format(engine=self._stt_engine_name),
            KEY_HINTS_TEXT,
        ]
        self.update(FIELD_SEPARATOR.join(fields))
