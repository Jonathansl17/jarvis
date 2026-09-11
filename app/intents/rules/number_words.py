"""Spelled-out Spanish cardinal numbers, for parsing free text.

Kept apart from `intents/rules/base.py` because the unit/ten/hundred/
multiplier tables are data, not extraction logic. Only units, tens, hundreds
and their combinations with "mil"/"millón"/"millones" are supported; a
fractional remainder such as "y medio" is silently dropped rather than
guessed at.
"""

import re
from dataclasses import dataclass

_UNITS = {
    "cero": 0, "uno": 1, "un": 1, "una": 1, "dos": 2, "tres": 3, "cuatro": 4,
    "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
}
_TEENS = {
    "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14,
    "quince": 15, "dieciseis": 16, "dieciséis": 16, "diecisiete": 17,
    "dieciocho": 18, "diecinueve": 19,
}
_TENS = {
    "veinte": 20, "veintiuno": 21, "veintidos": 22, "veintidós": 22,
    "treinta": 30, "cuarenta": 40, "cincuenta": 50, "sesenta": 60,
    "setenta": 70, "ochenta": 80, "noventa": 90,
}
_HUNDREDS = {
    "cien": 100, "ciento": 100, "doscientos": 200, "trescientos": 300,
    "cuatrocientos": 400, "quinientos": 500, "seiscientos": 600,
    "setecientos": 700, "ochocientos": 800, "novecientos": 900,
}
MULTIPLIERS = {
    "mil": 1_000, "millon": 1_000_000, "millón": 1_000_000, "millones": 1_000_000,
}
_CONNECTOR = "y"
_AMBIGUOUS_ARTICLE_UNO = "un"
_AMBIGUOUS_ARTICLE_UNA = "una"

_NUMBER_WORDS = {**_UNITS, **_TEENS, **_TENS, **_HUNDREDS}
_VOCABULARY = sorted(set(_NUMBER_WORDS) | set(MULTIPLIERS) | {_CONNECTOR}, key=len, reverse=True)
_WORD_ALTERNATION = "|".join(re.escape(word) for word in _VOCABULARY)
_WORD_RUN_PATTERN = re.compile(
    rf"\b(?:{_WORD_ALTERNATION})\b(?:\s+(?:{_WORD_ALTERNATION})\b)*",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class NumberWordMatch:
    """A spelled-out number phrase and the value it resolved to."""

    span: tuple[int, int]
    value: float


def find_number_words(text: str) -> list[NumberWordMatch]:
    """Return every spelled-out number phrase in `text` that parses cleanly."""
    matches = []
    for match in _WORD_RUN_PATTERN.finditer(text):
        value = _parse_run(match.group())
        if value is not None:
            matches.append(NumberWordMatch(span=match.span(), value=value))
    return matches


def _parse_run(run: str) -> float | None:
    """Parse one contiguous run of number/connector words, or None if invalid.

    Words are summed within a "group" (units, tens, hundreds) until a
    multiplier word scales the group and folds it into the running total, so
    "cuarenta mil doscientos" reduces to 40_000 + 200.
    """
    words = [word.lower() for word in run.split() if word.lower() != _CONNECTOR]
    if not words or words == [_AMBIGUOUS_ARTICLE_UNO] or words == [_AMBIGUOUS_ARTICLE_UNA]:
        # A bare "un"/"una" is almost always the Spanish indefinite article
        # ("un carro"), not the cardinal number one, so it is dropped rather
        # than guessed at, exactly like an unparsed fractional remainder.
        return None
    total, group = 0.0, 0.0
    for word in words:
        if word in MULTIPLIERS:
            total += (group or 1.0) * MULTIPLIERS[word]
            group = 0.0
        elif word in _NUMBER_WORDS:
            group += _NUMBER_WORDS[word]
        else:
            return None
    return total + group
