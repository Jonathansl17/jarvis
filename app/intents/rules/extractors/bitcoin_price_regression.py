"""Extracts bitcoin_price_regression fields from Spanish free text."""

from typing import Any, ClassVar

from app.intents.rules.base import find_number_near

_DAYS_KEYWORDS = ("dias", "días", "dia", "día")


class BitcoinPriceRegressionExtractor:
    """Extracts how many days ahead to forecast the bitcoin closing price."""

    required_fields: ClassVar[list[str]] = ["days"]

    def extract(self, text: str) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        days = find_number_near(text, _DAYS_KEYWORDS)
        if days is not None:
            fields["days"] = int(days)
        return fields
