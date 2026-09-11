"""Turns a prediction response body into Spanish reply text.

Branches on the three response *shapes* the API's models produce
(label/probability, single value, list of forecast points) rather than on
the model name, so an eleventh model needs no change here unless it
introduces a fourth shape.
"""

from typing import Any

from app.dialogue.prediction_replies import FORECAST_REPLIES, LABEL_REPLIES, SINGLE_VALUE_REPLIES
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

    Branches on `body`'s shape (forecast / label / single value), then looks
    up `model_name` in the per-model reply tables for the unit-aware wording;
    a model missing from a table still gets a serviceable generic reply.
    """
    if _FORECAST_KEY in body:
        return _format_forecast(model_name, body[_FORECAST_KEY])
    if _LABEL_KEY in body:
        return _format_label(model_name, body)
    return _format_single_value(model_name, body)


def _format_forecast(model_name: str, points: list[dict[str, Any]]) -> str:
    """Render a forecast via its model's table entry, or a generic fallback."""
    renderer = FORECAST_REPLIES.get(model_name)
    if renderer is not None:
        return renderer(points)
    lines = [FORECAST_POINT_TEMPLATE.format(**point) for point in points]
    return _LINE_SEPARATOR.join([FORECAST_INTRO_TEXT, *lines])


def _format_label(model_name: str, body: dict[str, Any]) -> str:
    """Render a classification result via its model's table entry, or a fallback."""
    renderer = LABEL_REPLIES.get(model_name)
    if renderer is not None:
        return renderer(body)
    return _format_label_generic(body)


def _format_label_generic(body: dict[str, Any]) -> str:
    """Fall back to an untranslated label, with probability when present."""
    probability = body.get(_PROBABILITY_KEY)
    if probability is None:
        return LABEL_ONLY_TEMPLATE.format(label=body[_LABEL_KEY])
    return LABEL_WITH_PROBABILITY_TEMPLATE.format(label=body[_LABEL_KEY], probability=probability)


def _format_single_value(model_name: str, body: dict[str, Any]) -> str:
    """Render a single-value regression result via its model's table entry."""
    renderer = SINGLE_VALUE_REPLIES.get(model_name)
    if renderer is not None:
        return renderer(body)
    value_field = next(key for key in body if key.startswith(_PREDICTED_VALUE_PREFIX))
    return VALUE_TEMPLATE.format(value=body[value_field])
