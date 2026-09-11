"""Spanish one-line description of each model, for Gemini's system prompt.

Synonyms reuse `intents.rules.registry.MODEL_KEYWORDS` so the trigger words
Gemini is told about and the ones the keyword-based fallback parser matches
never drift apart.
"""

from app.intents.gemini_inference_rules import build_model_rules_text
from app.intents.rules.registry import MODEL_KEYWORDS

MODEL_DESCRIPTIONS: dict[str, str] = {
    "car_price_regression": "precio de venta estimado de un carro usado",
    "body_fat_regression": "porcentaje de grasa corporal a partir de medidas corporales",
    "stroke_classification": "riesgo de sufrir un derrame cerebral (ACV)",
    "hepatitis_type_classification": "categoría de hepatitis C a partir de un panel de sangre",
    "cirrhosis_type_classification": "presencia y etapa de cirrosis hepática",
    "wine_quality_classification": "calidad de un vino a partir de sus medidas de laboratorio",
    "avocado_price_regression": "precio promedio de aguacates en una región y semana",
    "flight_delay_regression": "minutos de retraso estimados en la llegada de un vuelo",
    "telecom_churn_classification": "probabilidad de que un cliente de telefonía se dé de baja (churn)",
    "bitcoin_price_regression": "pronóstico del precio de cierre de bitcoin para los próximos días",
}

_CATALOG_LINE_TEMPLATE = "- {model_name}: {description} (sinónimos: {synonyms})"
_SYNONYM_SEPARATOR = ", "
_LINE_SEPARATOR = "\n"


def build_model_catalog_text() -> str:
    """Render every model as a description line plus its own inference rules."""
    lines = []
    for model_name, description in MODEL_DESCRIPTIONS.items():
        lines.append(
            _CATALOG_LINE_TEMPLATE.format(
                model_name=model_name,
                description=description,
                synonyms=_SYNONYM_SEPARATOR.join(MODEL_KEYWORDS[model_name]),
            )
        )
        rules_text = build_model_rules_text(model_name)
        if rules_text:
            lines.append(rules_text)
    return _LINE_SEPARATOR.join(lines)
