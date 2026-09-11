"""Extracts avocado_price_regression fields from Spanish free text."""

import re
from typing import Any, ClassVar

from app.intents.rules.base import find_literal
from app.intents.rules.dates import find_full_date
from app.intents.rules.quantities import find_number_immediately_before, find_quantity_near
from app.intents.rules.tables.avocado_regions import AVOCADO_REGION_ALIASES
from app.intents.rules.tables.calendar import MONTH_NAMES

_TYPE_ALIASES = {"conventional": ("convencional",), "organic": ("organico", "orgánico", "organica", "orgánica")}
_DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")

_NUMBER_FIELD_KEYWORDS: dict[str, tuple[str, ...]] = {
    "total_volume": ("volumen total", "volumen"),
    "total_bags": ("bolsas totales", "total de bolsas", "bolsas en total"),
    "small_bags": ("bolsas pequeñas", "bolsas pequenas"),
    "large_bags": ("bolsas grandes", "grandes"),
    "xlarge_bags": ("bolsas extra grandes", "bolsas xl", "extragrande", "extra grande"),
}

# The PLU code itself (e.g. "4046") is also a number in the text, so the
# quantity sold "of" it is matched with a strict "right before the phrase"
# search instead of `find_quantity_near`'s character-distance search, which
# would otherwise anchor to the PLU code rather than to its sales volume.
_PLU_CODE_PHRASES: dict[str, tuple[str, ...]] = {
    "plu_4046": ("del código 4046", "del codigo 4046", "del 4046"),
    "plu_4225": ("del código 4225", "del codigo 4225", "del 4225"),
    "plu_4770": ("del código 4770", "del codigo 4770", "del 4770"),
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
        region = find_literal(text, AVOCADO_REGION_ALIASES)
        if region is not None:
            fields["region"] = region
        date = _find_date(text)
        if date is not None:
            fields["date"] = date
        for field, keywords in _NUMBER_FIELD_KEYWORDS.items():
            value = find_quantity_near(text, keywords)
            if value is not None:
                fields[field] = value
        for field, phrases in _PLU_CODE_PHRASES.items():
            value = find_number_immediately_before(text, phrases)
            if value is not None:
                fields[field] = value
        return fields


def _find_date(text: str) -> str | None:
    """Return the sale week as an ISO date, from an explicit date or "hoy"."""
    date_match = _DATE_PATTERN.search(text)
    if date_match:
        return date_match.group()
    return find_full_date(text, MONTH_NAMES)
