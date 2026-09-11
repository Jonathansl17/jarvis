"""Extracts car_price_regression fields from Spanish free text."""

from typing import Any, ClassVar

from app.intents.rules.base import find_literal, find_number_near, find_year

_KMS_KEYWORDS = ("kilometro", "kilómetro", "kms", "km")
_PRICE_KEYWORDS = ("precio", "cuesta", "vale", "valor")
_OWNER_KEYWORDS = ("dueños anteriores", "dueños", "propietarios anteriores")

_FUEL_ALIASES = {
    "Petrol": ("gasolina", "petrol"),
    "Diesel": ("diesel", "diésel"),
    "CNG": ("gas natural", "cng"),
}
_SELLER_ALIASES = {
    "Dealer": ("agencia", "concesionario", "dealer"),
    "Individual": ("particular", "individual"),
}
_TRANSMISSION_ALIASES = {
    "Manual": ("manual",),
    "Automatic": ("automatico", "automático", "automatica", "automática"),
}


class CarPriceRegressionExtractor:
    """Extracts a used car's attributes from a Spanish description."""

    required_fields: ClassVar[list[str]] = [
        "present_price",
        "year",
        "kms_driven",
        "owner",
        "fuel_type",
        "seller_type",
        "transmission",
    ]

    def extract(self, text: str) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        self._add_numbers(text, fields)
        self._add_literals(text, fields)
        return fields

    @staticmethod
    def _add_numbers(text: str, fields: dict[str, Any]) -> None:
        year = find_year(text)
        if year is not None:
            fields["year"] = year
        kms = find_number_near(text, _KMS_KEYWORDS)
        if kms is not None:
            fields["kms_driven"] = kms
        price = find_number_near(text, _PRICE_KEYWORDS)
        if price is not None:
            fields["present_price"] = price
        owner = find_number_near(text, _OWNER_KEYWORDS)
        if owner is not None:
            fields["owner"] = int(owner)

    @staticmethod
    def _add_literals(text: str, fields: dict[str, Any]) -> None:
        fuel = find_literal(text, _FUEL_ALIASES)
        if fuel is not None:
            fields["fuel_type"] = fuel
        seller = find_literal(text, _SELLER_ALIASES)
        if seller is not None:
            fields["seller_type"] = seller
        transmission = find_literal(text, _TRANSMISSION_ALIASES)
        if transmission is not None:
            fields["transmission"] = transmission
