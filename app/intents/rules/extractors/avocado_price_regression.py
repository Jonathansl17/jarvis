"""Extracts avocado_price_regression fields from Spanish free text."""

import re
from typing import Any, ClassVar

from app.intents.rules.base import find_literal, find_number_near, find_value_after

_TYPE_ALIASES = {"conventional": ("convencional",), "organic": ("organico", "orgánico", "organica", "orgánica")}
_REGION_KEYWORDS = ("region", "región")
_DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")

_NUMBER_FIELD_KEYWORDS: dict[str, tuple[str, ...]] = {
    "total_volume": ("volumen total", "volumen"),
    "plu_4046": ("4046",),
    "plu_4225": ("4225",),
    "plu_4770": ("4770",),
    "total_bags": ("bolsas totales", "total de bolsas"),
    "small_bags": ("bolsas pequeñas", "bolsas pequenas"),
    "large_bags": ("bolsas grandes",),
    "xlarge_bags": ("bolsas extra grandes", "bolsas xl"),
}


class AvocadoPriceRegressionExtractor:
    """Extracts a week's sales volumes for one avocado type and region."""

    required_fields: ClassVar[list[str]] = [
        "type",
        "region",
        "date",
        "total_volume",
        "plu_4046",
        "plu_4225",
        "plu_4770",
        "total_bags",
        "small_bags",
        "large_bags",
        "xlarge_bags",
    ]

    def extract(self, text: str) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        avocado_type = find_literal(text, _TYPE_ALIASES)
        if avocado_type is not None:
            fields["type"] = avocado_type
        region = find_value_after(text, _REGION_KEYWORDS)
        if region is not None:
            fields["region"] = region
        date_match = _DATE_PATTERN.search(text)
        if date_match:
            fields["date"] = date_match.group()
        for field, keywords in _NUMBER_FIELD_KEYWORDS.items():
            value = find_number_near(text, keywords)
            if value is not None:
                fields[field] = value
        return fields
