"""Turns a prediction response body into Spanish reply text.

Branches on the three response *shapes* the API's models produce
(label/probability, single value, list of forecast points) rather than on
the model name, so an eleventh model needs no change here unless it
introduces a fourth shape.
"""

from typing import Any

from app.dialogue.strings import (
    FORECAST_INTRO_TEXT,
    FORECAST_POINT_TEMPLATE,
    LABEL_ONLY_TEMPLATE,
    LABEL_WITH_PROBABILITY_TEMPLATE,
    VALUE_TEMPLATE,
)

_FORECAST_KEY = "forecast"
_LABEL_KEY = "label"
_PROBABILITY_KEY = "probability"
_PREDICTED_VALUE_PREFIX = "predicted_"
_LINE_SEPARATOR = "\n"


def build_prediction_reply(model_name: str, body: dict[str, Any]) -> str:
    """Return the Spanish sentence describing one model's prediction body.

    `model_name` is accepted for interface symmetry with the caller but the
    formatting itself only looks at `body`'s shape.
    """
    if _FORECAST_KEY in body:
        return _format_forecast(body[_FORECAST_KEY])
    if _LABEL_KEY in body:
        return _format_label(body)
    return _format_single_value(body)


def _format_forecast(points: list[dict[str, Any]]) -> str:
    """Render a list of forecast points as one line per day."""
    lines = [FORECAST_POINT_TEMPLATE.format(**point) for point in points]
    return _LINE_SEPARATOR.join([FORECAST_INTRO_TEXT, *lines])


def _format_label(body: dict[str, Any]) -> str:
    """Render a classification result, with probability when present."""
    probability = body.get(_PROBABILITY_KEY)
    if probability is None:
        return LABEL_ONLY_TEMPLATE.format(label=body[_LABEL_KEY])
    return LABEL_WITH_PROBABILITY_TEMPLATE.format(label=body[_LABEL_KEY], probability=probability)


def _format_single_value(body: dict[str, Any]) -> str:
    """Render a single-value regression result, whatever its field is named."""
    value_field = next(key for key in body if key.startswith(_PREDICTED_VALUE_PREFIX))
    return VALUE_TEMPLATE.format(value=body[value_field])
