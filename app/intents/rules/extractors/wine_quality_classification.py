"""Extracts wine_quality_classification fields from Spanish free text."""

from typing import Any, ClassVar

from app.intents.rules.base import find_literal, find_number_near

_TYPE_ALIASES = {"red": ("tinto", "rojo"), "white": ("blanco",)}
_ALCOHOL_KEYWORDS = ("alcohol", "grados")
_DENSITY_KEYWORDS = ("densidad",)
_FREE_SO2_KEYWORDS = ("dioxido de azufre libre", "dióxido de azufre libre", "so2 libre")
_TOTAL_SO2_KEYWORDS = ("dioxido de azufre total", "dióxido de azufre total", "so2 total")
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
            ("free_sulfur_dioxide", _FREE_SO2_KEYWORDS),
            ("total_sulfur_dioxide", _TOTAL_SO2_KEYWORDS),
            ("volatile_acidity", _VOLATILE_ACIDITY_KEYWORDS),
            ("residual_sugar", _RESIDUAL_SUGAR_KEYWORDS),
        ):
            value = find_number_near(text, keywords)
            if value is not None:
                fields[field] = value
        return fields
