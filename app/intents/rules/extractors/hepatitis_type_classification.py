"""Extracts hepatitis_type_classification fields from Spanish free text."""

from typing import Any, ClassVar

from app.intents.rules.base import find_literal, find_number_near

_AGE_KEYWORDS = ("años", "anos", "edad")
_SEX_ALIASES = {"m": ("hombre", "masculino", "varon", "varón"), "f": ("mujer", "femenino")}

# Optional lab values: keyed by the wire field name, matched against its
# lowercase abbreviation appearing anywhere near a number in the text.
_OPTIONAL_LAB_KEYWORDS: dict[str, tuple[str, ...]] = {
    "ALB": ("albumina", "albúmina", "alb"),
    "ALP": ("fosfatasa alcalina", "alp"),
    "ALT": ("alt",),
    "AST": ("ast",),
    "BIL": ("bilirrubina", "bil"),
    "CHE": ("colinesterasa", "che"),
    "CHOL": ("colesterol", "chol"),
    "CREA": ("creatinina", "crea"),
    "GGT": ("ggt",),
    "PROT": ("proteinas totales", "proteínas totales", "prot"),
}


class HepatitisTypeClassificationExtractor:
    """Extracts a person's age, sex, and optional blood panel results."""

    required_fields: ClassVar[list[str]] = ["age", "sex"]

    def extract(self, text: str) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        age = find_number_near(text, _AGE_KEYWORDS)
        if age is not None:
            fields["age"] = age
        sex = find_literal(text, _SEX_ALIASES)
        if sex is not None:
            fields["sex"] = sex
        for field, keywords in _OPTIONAL_LAB_KEYWORDS.items():
            value = find_number_near(text, keywords)
            if value is not None:
                fields[field] = value
        return fields
