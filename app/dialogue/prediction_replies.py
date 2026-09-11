"""Per-model tables mapping a prediction body to its Spanish reply text.

Replaces branching on model name with dict lookups, so adding an eleventh
model means one new table entry, not a new `if` in `reply_builder.py`.
"""

from collections.abc import Callable
from typing import Any

from app.dialogue import strings
from app.dialogue.spanish_dates import format_spanish_date

_ValueRenderer = Callable[[dict[str, Any]], str]
_LabelRenderer = Callable[[dict[str, Any]], str]
_ForecastRenderer = Callable[[list[dict[str, Any]]], str]

_LABEL_KEY = "label"
_PROBABILITY_KEY = "probability"
_STAGE_KEY = "stage"


def _value_renderer(
    field: str, template: str, extra: Callable[[float], dict[str, Any]] | None = None
) -> _ValueRenderer:
    """Build a renderer that formats one numeric field with its unit template."""

    def render(body: dict[str, Any]) -> str:
        value = body[field]
        context: dict[str, Any] = {"value": value}
        if extra is not None:
            context.update(extra(value))
        return template.format(**context)

    return render


def _label_with_probability_renderer(template: str, translations: dict[str, str]) -> _LabelRenderer:
    """Build a renderer for a label + probability classifier reply."""

    def render(body: dict[str, Any]) -> str:
        label = translations.get(body[_LABEL_KEY], body[_LABEL_KEY])
        return template.format(label=label, probability=body[_PROBABILITY_KEY])

    return render


def _cirrhosis_renderer(body: dict[str, Any]) -> str:
    """Render the cirrhosis cascade's binary result, plus its stage when positive."""
    stage = body.get(_STAGE_KEY)
    if stage is None:
        return strings.CIRRHOSIS_NEGATIVE_TEXT
    return strings.CIRRHOSIS_POSITIVE_TEMPLATE.format(stage=stage)


def _bitcoin_forecast_renderer(points: list[dict[str, Any]]) -> str:
    """Render each forecast day as a sentence, then note the data's cutoff."""
    sentences = [
        strings.BITCOIN_FORECAST_POINT_TEMPLATE.format(date_text=format_spanish_date(point["date"]), **point)
        for point in points
    ]
    return strings.FORECAST_POINT_SEPARATOR.join([*sentences, strings.BITCOIN_DATA_CUTOFF_TEXT])


SINGLE_VALUE_REPLIES: dict[str, _ValueRenderer] = {
    "car_price_regression": _value_renderer(
        "predicted_price", strings.CAR_PRICE_TEMPLATE,
        extra=lambda value: {"rupees": value * strings.RUPEES_PER_LAKH},
    ),
    "body_fat_regression": _value_renderer("predicted_body_fat", strings.BODY_FAT_TEMPLATE),
    "avocado_price_regression": _value_renderer("predicted_price", strings.AVOCADO_PRICE_TEMPLATE),
    "flight_delay_regression": _value_renderer("predicted_delay_minutes", strings.FLIGHT_DELAY_TEMPLATE),
}

LABEL_REPLIES: dict[str, _LabelRenderer] = {
    "stroke_classification": _label_with_probability_renderer(
        strings.STROKE_TEMPLATE, strings.STROKE_LABEL_TRANSLATIONS
    ),
    "telecom_churn_classification": _label_with_probability_renderer(
        strings.CHURN_TEMPLATE, strings.CHURN_LABEL_TRANSLATIONS
    ),
    "hepatitis_type_classification": _label_with_probability_renderer(
        strings.HEPATITIS_TEMPLATE, strings.HEPATITIS_LABEL_TRANSLATIONS
    ),
    "wine_quality_classification": _label_with_probability_renderer(
        strings.WINE_QUALITY_TEMPLATE, strings.WINE_QUALITY_LABEL_TRANSLATIONS
    ),
    "cirrhosis_type_classification": _cirrhosis_renderer,
}

FORECAST_REPLIES: dict[str, _ForecastRenderer] = {
    "bitcoin_price_regression": _bitcoin_forecast_renderer,
}
