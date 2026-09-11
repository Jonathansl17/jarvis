"""Extracts stroke_classification fields from Spanish free text."""

from typing import Any, ClassVar

from app.intents.rules.base import find_boolean, find_literal, find_number_near

_AGE_KEYWORDS = ("años", "anos", "edad")
_GLUCOSE_KEYWORDS = ("glucosa",)
_BMI_KEYWORDS = ("imc", "masa corporal")

_HYPERTENSION_TRUE = (
    "hipertenso", "hipertensa", "hipertension", "hipertensión",
    "presion alta", "presión alta",
)
_HYPERTENSION_FALSE = (
    "sin hipertension", "sin hipertensión", "no es hipertenso", "no es hipertensa",
    "no tiene hipertension", "no tiene hipertensión",
)
_HEART_DISEASE_TRUE = (
    "enfermedad del corazon", "enfermedad del corazón", "enfermedad cardiaca",
    "enfermedad cardíaca", "problema del corazon", "problema cardiaco",
    "problema cardíaco", "cardiaco", "cardíaco",
)
_HEART_DISEASE_FALSE = (
    "sin enfermedad del corazon", "sin enfermedad del corazón",
    "sin enfermedad cardiaca", "sin enfermedad cardíaca",
    "sin problemas cardiacos", "sin problemas cardíacos",
    "no tiene problemas del corazon", "no tiene enfermedad del corazon",
)

_GENDER_ALIASES = {"Male": ("hombre", "masculino", "varon", "varón"), "Female": ("mujer", "femenino")}
_MARRIED_ALIASES = {"Yes": ("casado", "casada"), "No": ("soltero", "soltera")}
_WORK_TYPE_ALIASES = {
    "Govt_job": ("empleado publico", "empleado público", "gobierno"),
    "Private": ("empresa privada", "privado"),
    "Self-employed": ("independiente", "cuenta propia", "autonomo", "autónomo"),
    "children": ("niño", "niña", "menor de edad"),
    "Never_worked": ("nunca ha trabajado",),
}
_RESIDENCE_ALIASES = {"Urban": ("urbano", "ciudad"), "Rural": ("rural", "campo")}
_SMOKING_ALIASES = {
    "formerly smoked": ("exfumador", "dejo de fumar", "dejó de fumar"),
    "never smoked": ("nunca fumo", "nunca fumó", "no fuma"),
    "smokes": ("fuma", "fumador"),
    "Unknown": ("desconocido",),
}


class StrokeClassificationExtractor:
    """Extracts a person's medical and lifestyle facts for stroke risk."""

    required_fields: ClassVar[list[str]] = [
        "gender",
        "age",
        "hypertension",
        "heart_disease",
        "ever_married",
        "work_type",
        "Residence_type",
        "avg_glucose_level",
        "smoking_status",
    ]

    def extract(self, text: str) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        self._add_numbers(text, fields)
        self._add_booleans(text, fields)
        self._add_literals(text, fields)
        return fields

    @staticmethod
    def _add_numbers(text: str, fields: dict[str, Any]) -> None:
        age = find_number_near(text, _AGE_KEYWORDS)
        if age is not None:
            fields["age"] = age
        glucose = find_number_near(text, _GLUCOSE_KEYWORDS)
        if glucose is not None:
            fields["avg_glucose_level"] = glucose
        bmi = find_number_near(text, _BMI_KEYWORDS)
        if bmi is not None:
            fields["bmi"] = bmi

    @staticmethod
    def _add_booleans(text: str, fields: dict[str, Any]) -> None:
        hypertension = find_boolean(text, _HYPERTENSION_TRUE, _HYPERTENSION_FALSE)
        if hypertension is not None:
            fields["hypertension"] = hypertension
        heart_disease = find_boolean(text, _HEART_DISEASE_TRUE, _HEART_DISEASE_FALSE)
        if heart_disease is not None:
            fields["heart_disease"] = heart_disease

    @staticmethod
    def _add_literals(text: str, fields: dict[str, Any]) -> None:
        for field, aliases in (
            ("gender", _GENDER_ALIASES),
            ("ever_married", _MARRIED_ALIASES),
            ("work_type", _WORK_TYPE_ALIASES),
            ("Residence_type", _RESIDENCE_ALIASES),
            ("smoking_status", _SMOKING_ALIASES),
        ):
            value = find_literal(text, aliases)
            if value is not None:
                fields[field] = value
