"""Digit-written number parsing shared by every numeric-extraction helper,
mirroring `number_words.py`'s handling of the spelled-out equivalent.
"""

import re

from app.intents.rules.number_words import MULTIPLIERS

MULTIPLIER_ALTERNATION = "|".join(re.escape(word) for word in MULTIPLIERS)
NUMBER_PATTERN = re.compile(
    rf"\b(?P<value>\d+(?:[.,]\d+)?)\s*(?P<multiplier>{MULTIPLIER_ALTERNATION})?\b",
    re.IGNORECASE,
)


def digit_value(match: re.Match[str]) -> float:
    """Return one number match's value, scaled by its multiplier.

    The digit itself is optional so a caller matching a bare multiplier word
    ("mil" alone meaning one thousand) can still use this; `NUMBER_PATTERN`
    itself always requires a digit, so its own matches never hit that case.
    """
    digits = match.group("value")
    value = float(digits.replace(",", ".")) if digits else 1.0
    multiplier = match.group("multiplier")
    return value * MULTIPLIERS[multiplier.lower()] if multiplier else value


def find_digit_candidates(text: str) -> list[tuple[tuple[int, int], float]]:
    """Return every digit-written number in `text`, scaled by its multiplier."""
    return [(match.span(), digit_value(match)) for match in NUMBER_PATTERN.finditer(text)]
