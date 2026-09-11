"""Shared contract and framework-free helpers for keyword-based field
extraction, mirroring `api/app/adapters/base.py`'s split of a Protocol plus
small helpers used by every implementation.
"""

import re
from typing import Any, ClassVar, Protocol

from app.intents.rules.number_words import MULTIPLIERS, find_number_words

_DIGIT_MULTIPLIER_ALTERNATION = "|".join(re.escape(word) for word in MULTIPLIERS)
_NUMBER_PATTERN = re.compile(
    rf"\b(?P<value>\d+(?:[.,]\d+)?)\s*(?P<multiplier>{_DIGIT_MULTIPLIER_ALTERNATION})?\b",
    re.IGNORECASE,
)
_YEAR_PATTERN = re.compile(r"\b(19|20)\d{2}\b")
_WORD_PATTERN = re.compile(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]+")
_MAX_KEYWORD_DISTANCE = 15


class FieldExtractor(Protocol):
    """Pulls one model's fields out of Spanish free text, no network I/O."""

    required_fields: ClassVar[list[str]]

    def extract(self, text: str) -> dict[str, Any]: ...


def find_literal(text: str, aliases: dict[str, tuple[str, ...]]) -> str | None:
    """Return the canonical value whose Spanish alias appears first in `text`."""
    lowered = text.lower()
    for canonical, alias_list in aliases.items():
        if any(alias in lowered for alias in alias_list):
            return canonical
    return None


def find_boolean(text: str, true_keywords: tuple[str, ...], false_keywords: tuple[str, ...]) -> bool | None:
    """Return True/False for the first boolean cue phrase found, else None."""
    lowered = text.lower()
    if any(keyword in lowered for keyword in false_keywords):
        return False
    if any(keyword in lowered for keyword in true_keywords):
        return True
    return None


def find_number_near(text: str, keywords: tuple[str, ...]) -> float | None:
    """Return the number closest to one of `keywords`, or None if none fits.

    Candidates come from digits (with an optional "mil"/"millón(es)" suffix)
    and from spelled-out Spanish number words, ranked by their character
    distance to the nearest keyword occurrence, so an unrelated number
    elsewhere in the sentence is not mistaken for the wanted field. A number
    word phrase that cannot be parsed is never a candidate, so it is never
    returned as a wrong guess.
    """
    candidates = _digit_candidates(text) + _word_candidates(text)
    if not candidates:
        return None
    lowered = text.lower()
    best_value, best_distance = None, None
    for keyword in keywords:
        index = lowered.find(keyword)
        if index == -1:
            continue
        for span, value in candidates:
            distance = _distance_to_span(span, index, len(keyword))
            if distance <= _MAX_KEYWORD_DISTANCE and (best_distance is None or distance < best_distance):
                best_value, best_distance = value, distance
    return best_value


def parse_bare_number(text: str) -> float | None:
    """Return `text` as a number if it is nothing but one number, else None.

    Unlike `find_number_near`, this needs no keyword: it is for a short,
    literal answer to a missing-field prompt (e.g. just "2"), where no
    keyword is present in the answer itself to anchor the search.
    """
    stripped = text.strip()
    if not stripped:
        return None
    digit_match = _NUMBER_PATTERN.fullmatch(stripped)
    if digit_match:
        return _digit_value(digit_match)
    word_matches = find_number_words(stripped)
    if len(word_matches) == 1 and word_matches[0].span == (0, len(stripped)):
        return word_matches[0].value
    return None


def _digit_value(match: re.Match[str]) -> float:
    """Return one `_NUMBER_PATTERN` match's value, scaled by its multiplier."""
    value = float(match.group("value").replace(",", "."))
    multiplier = match.group("multiplier")
    return value * MULTIPLIERS[multiplier.lower()] if multiplier else value


def _digit_candidates(text: str) -> list[tuple[tuple[int, int], float]]:
    """Return every digit-written number in `text`, scaled by its multiplier."""
    return [(match.span(), _digit_value(match)) for match in _NUMBER_PATTERN.finditer(text)]


def _word_candidates(text: str) -> list[tuple[tuple[int, int], float]]:
    """Return every spelled-out number word phrase in `text`."""
    return [(match.span, match.value) for match in find_number_words(text)]


def _distance_to_span(span: tuple[int, int], keyword_index: int, keyword_length: int) -> int:
    """Return the character gap between a number's span and a keyword span."""
    start, end = span
    keyword_end = keyword_index + keyword_length
    if end <= keyword_index:
        return keyword_index - end
    if start >= keyword_end:
        return start - keyword_end
    return 0


def find_year(text: str) -> int | None:
    """Return the first four-digit year found in `text`, if any."""
    match = _YEAR_PATTERN.search(text)
    return int(match.group()) if match else None


def find_value_after(text: str, keywords: tuple[str, ...]) -> str | None:
    """Return the capitalized word right after one of `keywords`, if present."""
    lowered = text.lower()
    for keyword in keywords:
        index = lowered.find(keyword)
        if index == -1:
            continue
        remainder = text[index + len(keyword) :].strip()
        match = _WORD_PATTERN.match(remainder)
        if match:
            return match.group().capitalize()
    return None


def find_from_table(text: str, table: dict[str, int]) -> int | None:
    """Return the integer mapped from the first table key found in `text`."""
    lowered = text.lower()
    for key, value in table.items():
        if key in lowered:
            return value
    return None
