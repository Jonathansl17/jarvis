"""Extracts car_price_regression fields from Spanish free text."""

from typing import Any, ClassVar

from app.intents.rules.base import find_from_table, find_literal, find_number_near, find_year

_KMS_KEYWORDS = ("kilometro", "kilómetro", "kms", "km")
# "costó"/"costo" come first: they name the car's own price, whereas "vale" or
# "cuesta" also show up in the surrounding question ("¿cuánto vale...?") next
# to unrelated words, so checking them first avoids anchoring to the wrong
# number when both keywords are equally close to some number in the text.
_PRICE_KEYWORDS = ("costo", "costó", "precio", "valor", "cuesta", "vale")
_OWNER_KEYWORDS = ("dueños anteriores", "dueños", "propietarios anteriores")
_DEFAULT_OWNER_COUNT = 0
_OWNER_COUNT_TABLE: dict[str, int] = {
    "un solo dueño": _DEFAULT_OWNER_COUNT, "un solo dueno": _DEFAULT_OWNER_COUNT,
    "unico dueño": _DEFAULT_OWNER_COUNT, "único dueño": _DEFAULT_OWNER_COUNT,
    "primer dueño": _DEFAULT_OWNER_COUNT, "primer propietario": _DEFAULT_OWNER_COUNT,
    "segundo dueño": 1, "segunda dueña": 1, "segundo propietario": 1,
    "tercer dueño": 2, "tercer propietario": 2,
}

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
        fields["owner"] = _find_owner_count(text)

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


def _find_owner_count(text: str) -> int:
    """Return the number of previous owners, defaulting to 0 when unstated.

    A used-car listing that never mentions a previous owner is read as a
    first-owner ("un solo dueño") car, matching the dataset's own baseline.
    """
    named_count = find_from_table(text, _OWNER_COUNT_TABLE)
    if named_count is not None:
        return named_count
    counted = find_number_near(text, _OWNER_KEYWORDS)
    return int(counted) if counted is not None else _DEFAULT_OWNER_COUNT
