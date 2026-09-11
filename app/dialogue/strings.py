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

# Bitcoin's forecast is trained on data through July 2017, so its reply
# reads as a continuation of that series rather than a live quote.
BITCOIN_FORECAST_POINT_TEMPLATE = (
    "Para el {date_text} el precio del bitcoin se aproxima a {price:,.0f} dólares, "
    "entre {lower:,.0f} y {upper:,.0f}."
)
BITCOIN_DATA_CUTOFF_TEXT = (
    "Los datos de entrenamiento llegan hasta julio de 2017, así que el pronóstico "
    "continúa esa serie."
)
FORECAST_POINT_SEPARATOR = " "

# Generic fallbacks, used only for a model with no entry in
# `prediction_replies.py`'s tables, so an eleventh model never crashes here.
LABEL_WITH_PROBABILITY_TEMPLATE = "El resultado es {label}, con una confianza de {probability:.0%}."
LABEL_ONLY_TEMPLATE = "El resultado es {label}."
VALUE_TEMPLATE = "El valor estimado es {value:.2f}."
FORECAST_INTRO_TEXT = "Este es el pronóstico solicitado:"
FORECAST_POINT_TEMPLATE = "{date}: {price:.2f} (entre {lower:.2f} y {upper:.2f})"

# How many rupees one lakh is worth, for the car price reply's rupee aside.
RUPEES_PER_LAKH = 100_000

# Single-value regression replies, one per model, each stating its unit in a
# natural Spanish sentence.
CAR_PRICE_TEMPLATE = (
    "El carro se vendería por unos {value:.2f} lakhs de rupias, cerca de {rupees:,.0f} rupias."
)
BODY_FAT_TEMPLATE = "Tu porcentaje de grasa corporal estaría alrededor de {value:.1f} %."
AVOCADO_PRICE_TEMPLATE = "El precio promedio estimado del aguacate es de {value:.2f} dólares."
FLIGHT_DELAY_TEMPLATE = "El vuelo llegaría con un retraso estimado de {value:.0f} minutos."

# Classifier replies, one per model, naming the label and its probability in
# a natural Spanish sentence.
STROKE_TEMPLATE = "El riesgo de derrame es {label}: probabilidad {probability:.2f}."
CHURN_TEMPLATE = "Es {label} que el cliente se vaya: probabilidad {probability:.2f}."
HEPATITIS_TEMPLATE = "El panel sugiere {label}, con una probabilidad de {probability:.2f}."
WINE_QUALITY_TEMPLATE = "La calidad estimada del vino es {label}."
CIRRHOSIS_NEGATIVE_TEXT = "No se detectan indicios de cirrosis."
CIRRHOSIS_POSITIVE_TEMPLATE = "El paciente tendría cirrosis, en la etapa {stage}."

# Raw label -> Spanish phrase, one table per classifier since each reads
# naturally with different wording for the same yes/no distinction.
STROKE_LABEL_TRANSLATIONS = {"stroke": "alto", "no stroke": "bajo"}
CHURN_LABEL_TRANSLATIONS = {"churn": "probable", "no churn": "poco probable"}
HEPATITIS_LABEL_TRANSLATIONS = {
    "Blood Donor": "un donante sano",
    "Hepatitis": "hepatitis",
    "Fibrosis": "fibrosis",
    "Cirrhosis": "cirrosis",
}
WINE_QUALITY_LABEL_TRANSLATIONS = {"low": "baja", "medium": "media", "high": "alta"}
