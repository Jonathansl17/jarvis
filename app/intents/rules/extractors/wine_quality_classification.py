"""Extracts wine_quality_classification fields from Spanish free text."""

from typing import Any, ClassVar

from app.intents.rules.base import find_literal, find_number_near
from app.intents.rules.quantities import find_number_immediately_before

_TYPE_ALIASES = {"red": ("tinto", "rojo"), "white": ("blanco",)}
_ALCOHOL_KEYWORDS = ("alcohol", "grados")
_DENSITY_KEYWORDS = ("densidad",)
_FREE_SO2_PHRASES = ("dioxido de azufre libre", "dióxido de azufre libre", "so2 libre")
_TOTAL_SO2_PHRASES = ("dioxido de azufre total", "dióxido de azufre total", "so2 total")
_VOLATILE_ACIDITY_KEYWORDS = ("acidez volatil", "acidez volátil")
_RESIDUAL_SUGAR_KEYWORDS = ("azucar residual", "azúcar residual")


class WineQualityClassificationExtractor:
    """Extracts a wine's colour and laboratory measurements."""

    required_fields: ClassVar[list[str]] = [
        "type",
        "free_sulfur_dioxide",
        "total_sulfur_dioxide",
        "density",
        "alcohol",
    ]

    def extract(self, text: str) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        wine_type = find_literal(text, _TYPE_ALIASES)
        if wine_type is not None:
            fields["type"] = wine_type
        for field, keywords in (
            ("alcohol", _ALCOHOL_KEYWORDS),
            ("density", _DENSITY_KEYWORDS),
            ("volatile_acidity", _VOLATILE_ACIDITY_KEYWORDS),
            ("residual_sugar", _RESIDUAL_SUGAR_KEYWORDS),
        ):
            value = find_number_near(text, keywords)
            if value is not None:
                fields[field] = value
        # The free and total SO2 readings are adjacent, identically shaped
        # clauses ("<n> de dióxido de azufre libre/total"), so a strict
        # "right before the phrase" match is used instead of `find_number_near`
        # to keep one clause's number from bleeding into the other.
        for field, phrases in (
            ("free_sulfur_dioxide", _FREE_SO2_PHRASES),
            ("total_sulfur_dioxide", _TOTAL_SO2_PHRASES),
        ):
            value = find_number_immediately_before(text, phrases)
            if value is not None:
                fields[field] = value
        return fields
