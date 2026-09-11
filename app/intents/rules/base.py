"""Shared contract and framework-free helpers for keyword-based field
extraction, mirroring `api/app/adapters/base.py`'s split of a Protocol plus
small helpers used by every implementation.
"""

import re
from typing import Any, ClassVar, Protocol

_NUMBER_PATTERN = re.compile(r"\b(?P<value>\d+(?:[.,]\d+)?)\s*(?P<thousand>mil)?\b", re.IGNORECASE)
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
    """Return the number closest to one of `keywords`, "mil" meaning x1000.

    Numbers are matched on full word boundaries first, then ranked by their
    character distance to the nearest keyword occurrence, so an unrelated
    number elsewhere in the sentence is not mistaken for the wanted field.
    """
    numbers = list(_NUMBER_PATTERN.finditer(text))
    if not numbers:
        return None
    lowered = text.lower()
    best_match, best_distance = None, None
    for keyword in keywords:
        index = lowered.find(keyword)
        if index == -1:
            continue
        for match in numbers:
            distance = _distance_to_keyword(match, index, len(keyword))
            if distance <= _MAX_KEYWORD_DISTANCE and (best_distance is None or distance < best_distance):
                best_match, best_distance = match, distance
    if best_match is None:
        return None
    value = float(best_match.group("value").replace(",", "."))
    return value * 1000 if best_match.group("thousand") else value


def _distance_to_keyword(match: re.Match[str], keyword_index: int, keyword_length: int) -> int:
    """Return the character gap between a number match and a keyword span."""
    keyword_end = keyword_index + keyword_length
    if match.end() <= keyword_index:
        return keyword_index - match.end()
    if match.start() >= keyword_end:
        return match.start() - keyword_end
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
