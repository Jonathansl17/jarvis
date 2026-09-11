"""Extracts telecom_churn_classification fields from Spanish free text."""

from typing import Any, ClassVar

from app.intents.rules.base import find_boolean, find_literal, find_number_near

_YES_NO_ALIASES = {"Yes": ("si", "sí"), "No": ("no",)}
_GENDER_ALIASES = {"Male": ("hombre", "masculino"), "Female": ("mujer", "femenino")}
_INTERNET_ALIASES = {"DSL": ("dsl",), "Fiber optic": ("fibra optica", "fibra óptica"), "No": ("sin internet",)}
_CONTRACT_ALIASES = {
    "Month-to-month": ("mes a mes",),
    "One year": ("un año", "un ano"),
    "Two year": ("dos años", "dos anos"),
}
_PAYMENT_ALIASES = {
    "Bank transfer (automatic)": ("transferencia bancaria",),
    "Credit card (automatic)": ("tarjeta de credito", "tarjeta de crédito"),
    "Electronic check": ("cheque electronico", "cheque electrónico"),
    "Mailed check": ("cheque por correo",),
}
_SENIOR_TRUE = ("adulto mayor", "tercera edad")
_SENIOR_FALSE = ("joven", "no es adulto mayor")
_TENURE_KEYWORDS = ("meses de antiguedad", "meses como cliente", "antiguedad", "antigüedad")
_MONTHLY_CHARGE_KEYWORDS = ("cargo mensual", "factura mensual", "mensualidad")

# Literal fields that reuse the plain yes/no alias table.
_YES_NO_FIELDS = (
    "Partner", "Dependents", "PhoneService", "MultipleLines", "OnlineSecurity",
    "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
    "StreamingMovies", "PaperlessBilling",
)


class TelecomChurnClassificationExtractor:
    """Extracts a subscriber's account and service attributes."""

    required_fields: ClassVar[list[str]] = [
        "gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService",
        "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
        "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
        "Contract", "PaperlessBilling", "PaymentMethod", "tenure", "MonthlyCharges",
    ]

    def extract(self, text: str) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        self._add_numbers(text, fields)
        self._add_literals(text, fields)
        return fields

    @staticmethod
    def _add_numbers(text: str, fields: dict[str, Any]) -> None:
        senior = find_boolean(text, _SENIOR_TRUE, _SENIOR_FALSE)
        if senior is not None:
            fields["SeniorCitizen"] = senior
        tenure = find_number_near(text, _TENURE_KEYWORDS)
        if tenure is not None:
            fields["tenure"] = tenure
        monthly_charges = find_number_near(text, _MONTHLY_CHARGE_KEYWORDS)
        if monthly_charges is not None:
            fields["MonthlyCharges"] = monthly_charges

    @staticmethod
    def _add_literals(text: str, fields: dict[str, Any]) -> None:
        gender = find_literal(text, _GENDER_ALIASES)
        if gender is not None:
            fields["gender"] = gender
        internet = find_literal(text, _INTERNET_ALIASES)
        if internet is not None:
            fields["InternetService"] = internet
        contract = find_literal(text, _CONTRACT_ALIASES)
        if contract is not None:
            fields["Contract"] = contract
        payment = find_literal(text, _PAYMENT_ALIASES)
        if payment is not None:
            fields["PaymentMethod"] = payment
        for field in _YES_NO_FIELDS:
            value = find_literal(text, _YES_NO_ALIASES)
            if value is not None:
                fields[field] = value
