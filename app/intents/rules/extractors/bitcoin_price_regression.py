"""Extracts bitcoin_price_regression fields from Spanish free text."""

from typing import Any, ClassVar

from app.intents.rules.base import find_number_near
from app.intents.rules.lookup import find_value_by_longest_key

_DAYS_KEYWORDS = ("dias", "días", "dia", "día")
# Spoken horizons that carry no digit, longest phrase wins on overlap.
_HORIZON_DAYS = {
    "pasado mañana": 2,
    "pasado manana": 2,
    "mañana": 1,
    "manana": 1,
    "una semana": 7,
    "la semana": 7,
    "quince dias": 15,
    "quince días": 15,
    "un mes": 30,
}


class BitcoinPriceRegressionExtractor:
    """Extracts how many days ahead to forecast the bitcoin closing price."""

    required_fields: ClassVar[list[str]] = ["days"]

    def extract(self, text: str) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        days = find_number_near(text, _DAYS_KEYWORDS)
        if days is None:
            days = find_value_by_longest_key(text, _HORIZON_DAYS)
        if days is not None:
            fields["days"] = int(days)
        return fields
