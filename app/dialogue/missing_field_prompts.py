"""Spanish question text asked for one missing model field.

One entry per field name used across `intents/rules/extractors/*.py`'s
`required_fields`. A field absent from the table still gets a serviceable
question from its humanized name, so a future eleventh model never crashes
this lookup.
"""

from app.dialogue.strings import MISSING_FIELD_PREFIX

_FIELD_QUESTIONS: dict[str, str] = {
    # car_price_regression
    "present_price": "¿cuál es el precio actual del vehículo?",
    "year": "¿de qué año es?",
    "kms_driven": "¿cuántos kilómetros tiene recorridos?",
    "owner": "¿cuántos dueños anteriores ha tenido?",
    "fuel_type": "¿qué tipo de combustible usa (gasolina, diésel o gas natural)?",
    "seller_type": "¿lo vende una agencia o un particular?",
    "transmission": "¿la transmisión es manual o automática?",
    # body_fat_regression
    "abdomen": "¿cuál es la circunferencia del abdomen, en centímetros?",
    "weight": "¿cuál es el peso, en kilogramos?",
    "wrist": "¿cuál es la circunferencia de la muñeca, en centímetros?",
    # stroke_classification / shared: gender, age
    "gender": "¿es hombre o mujer?",
    "age": "¿cuál es la edad?",
    "hypertension": "¿tiene hipertensión?",
    "heart_disease": "¿tiene alguna enfermedad cardíaca?",
    "ever_married": "¿está o ha estado casado/a?",
    "work_type": "¿a qué se dedica (gobierno, empresa privada, independiente)?",
    "Residence_type": "¿vive en una zona urbana o rural?",
    "avg_glucose_level": "¿cuál es el nivel promedio de glucosa?",
    "smoking_status": "¿fuma, fumó antes, o nunca ha fumado?",
    # hepatitis_type_classification / cirrhosis_type_classification
    "sex": "¿es hombre o mujer?",
    "edema": "¿presenta edema?",
    # wine_quality_classification
    "type": "¿es vino tinto o blanco (o, para aguacates, convencional u orgánico)?",
    "free_sulfur_dioxide": "¿cuál es el nivel de dióxido de azufre libre?",
    "total_sulfur_dioxide": "¿cuál es el nivel total de dióxido de azufre?",
    "density": "¿cuál es la densidad?",
    "alcohol": "¿cuál es el porcentaje de alcohol?",
    # avocado_price_regression
    "region": "¿de qué región son los datos?",
    "date": "¿de qué fecha son los datos (AAAA-MM-DD)?",
    "total_volume": "¿cuál fue el volumen total vendido?",
    "plu_4046": "¿cuántas unidades del código PLU 4046 se vendieron?",
    "plu_4225": "¿cuántas unidades del código PLU 4225 se vendieron?",
    "plu_4770": "¿cuántas unidades del código PLU 4770 se vendieron?",
    "total_bags": "¿cuántas bolsas en total se vendieron?",
    "small_bags": "¿cuántas bolsas pequeñas se vendieron?",
    "large_bags": "¿cuántas bolsas grandes se vendieron?",
    "xlarge_bags": "¿cuántas bolsas extra grandes se vendieron?",
    # flight_delay_regression
    "month": "¿en qué mes es el vuelo?",
    "day_of_month": "¿qué día del mes es el vuelo?",
    "day_of_week": "¿qué día de la semana es el vuelo?",
    "dep_hour": "¿a qué hora sale el vuelo?",
    "carrier": "¿con qué aerolínea es el vuelo?",
    "origin": "¿cuál es el aeropuerto de origen?",
    "dest": "¿cuál es el aeropuerto de destino?",
    "distance": "¿cuál es la distancia del vuelo?",
    # telecom_churn_classification
    "SeniorCitizen": "¿es una persona adulta mayor?",
    "Partner": "¿tiene pareja?",
    "Dependents": "¿tiene dependientes?",
    "PhoneService": "¿tiene servicio telefónico?",
    "MultipleLines": "¿tiene múltiples líneas?",
    "InternetService": "¿qué tipo de internet tiene (DSL, fibra óptica o ninguno)?",
    "OnlineSecurity": "¿tiene seguridad en línea contratada?",
    "OnlineBackup": "¿tiene respaldo en línea contratado?",
    "DeviceProtection": "¿tiene protección de dispositivo contratada?",
    "TechSupport": "¿tiene soporte técnico contratado?",
    "StreamingTV": "¿tiene streaming de TV contratado?",
    "StreamingMovies": "¿tiene streaming de películas contratado?",
    "Contract": "¿qué tipo de contrato tiene (mensual, un año o dos años)?",
    "PaperlessBilling": "¿tiene facturación electrónica?",
    "PaymentMethod": "¿cuál es su método de pago?",
    "tenure": "¿cuántos meses lleva como cliente?",
    "MonthlyCharges": "¿cuánto paga mensualmente?",
    # bitcoin_price_regression
    "days": "¿para cuántos días quieres el pronóstico?",
}


def build_missing_field_question(field: str) -> str:
    """Return the full Spanish question the assistant asks for `field`."""
    question = _FIELD_QUESTIONS.get(field, f"¿cuál es el valor de {_humanize(field)}?")
    return f"{MISSING_FIELD_PREFIX}{question}"


def _humanize(field: str) -> str:
    """Fall back to a readable label for a field missing from the table."""
    return field.replace("_", " ").lower()
