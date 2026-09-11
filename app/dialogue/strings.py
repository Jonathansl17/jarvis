"""Every Spanish phrase the assistant produces outside of a field prompt.

Kept in one place so no user-facing text is ever inlined at a call site.
Missing-field questions have their own table in `missing_field_prompts.py`,
one field per line, which would otherwise crowd this module.
"""

GREETING_TEXT = "Hola, soy JarvisTEC. ¿En qué modelo te puedo ayudar hoy?"
NOT_UNDERSTOOD_TEXT = "No entendí esa solicitud. ¿Puedes reformularla?"
EMPTY_TRANSCRIPT_TEXT = "No entendí lo que dijiste. ¿Puedes repetirlo?"
PREDICTION_ERROR_TEXT = "No pude comunicarme con el servicio de predicción. Intenta de nuevo."

MISSING_FIELD_PREFIX = "Necesito un dato más: "

FORECAST_INTRO_TEXT = "Este es el pronóstico solicitado:"
FORECAST_POINT_TEMPLATE = "{date}: {price:.2f} (entre {lower:.2f} y {upper:.2f})"
LABEL_WITH_PROBABILITY_TEMPLATE = "El resultado es {label}, con una confianza de {probability:.0%}."
LABEL_ONLY_TEMPLATE = "El resultado es {label}."
VALUE_TEMPLATE = "El valor estimado es {value:.2f}."
