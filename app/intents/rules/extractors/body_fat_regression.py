"""Extracts body_fat_regression fields from Spanish free text."""

from typing import Any, ClassVar

from app.intents.rules.base import find_number_near

_ABDOMEN_KEYWORDS = ("abdomen", "cintura")
_WEIGHT_KEYWORDS = ("peso", "kilogramos", "kg")
_WRIST_KEYWORDS = ("muñeca", "muneca")


class BodyFatRegressionExtractor:
    """Extracts the three body measurements the model needs."""

    required_fields: ClassVar[list[str]] = ["abdomen", "weight", "wrist"]

    def extract(self, text: str) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        abdomen = find_number_near(text, _ABDOMEN_KEYWORDS)
        if abdomen is not None:
            fields["abdomen"] = abdomen
        weight = find_number_near(text, _WEIGHT_KEYWORDS)
        if weight is not None:
            fields["weight"] = weight
        wrist = find_number_near(text, _WRIST_KEYWORDS)
        if wrist is not None:
            fields["wrist"] = wrist
        return fields
