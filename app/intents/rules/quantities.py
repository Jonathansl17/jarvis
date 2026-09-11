"""Numeric extraction beyond `base.py`'s generic `find_number_near`: an
explicit-zero cue ("ninguna", "cero") and a strict "right before the phrase"
match for adjacent, identically shaped clauses that would otherwise be
ambiguous by character distance alone.
"""

import re

from app.intents.rules.base import find_number_near
from app.intents.rules.digit_numbers import MULTIPLIER_ALTERNATION, digit_value

_ZERO_CUE_WORDS = ("ninguna", "ninguno", "cero", "nada de")
_ZERO_CUE_WINDOW = 20
# The digit is optional so a bare multiplier ("mil del 4770") still matches,
# mirroring `number_words.py`'s own "mil" alone meaning one thousand.
_NUMBER_BEFORE_PATTERN = (
    rf"(?P<value>\d+(?:[.,]\d+)?)?\s*(?P<multiplier>{MULTIPLIER_ALTERNATION})?\s*(?:de\s+)?{{phrase}}"
)


def find_quantity_near(text: str, keywords: tuple[str, ...]) -> float | None:
    """Return the number near `keywords`, treating a "none of it" cue as zero.

    Complements `find_number_near`: a phrase like "ninguna extragrande"
    states an explicit zero quantity with no digit or number word for that
    helper to find.
    """
    number = find_number_near(text, keywords)
    if number is not None:
        return number
    return _find_zero_cue(text, keywords)


def _find_zero_cue(text: str, keywords: tuple[str, ...]) -> float | None:
    """Return 0.0 if a zero-quantity cue word sits right before `keywords`."""
    lowered = text.lower()
    for keyword in keywords:
        index = lowered.find(keyword)
        if index == -1:
            continue
        window = lowered[max(0, index - _ZERO_CUE_WINDOW) : index]
        if any(word in window for word in _ZERO_CUE_WORDS):
            return 0.0
    return None


def find_number_immediately_before(text: str, phrases: tuple[str, ...]) -> float | None:
    """Return the number right before a "<number> de <phrase>" clause.

    Unlike `find_number_near`'s character-distance search, this requires
    strict adjacency, so two consecutive "<number> de <label>" clauses (e.g.
    two sulfur dioxide readings back to back) never bleed into each other.
    """
    lowered = text.lower()
    for phrase in phrases:
        pattern = re.compile(_NUMBER_BEFORE_PATTERN.format(phrase=re.escape(phrase)), re.IGNORECASE)
        match = pattern.search(lowered)
        if match and (match.group("value") or match.group("multiplier")):
            return digit_value(match)
    return None
