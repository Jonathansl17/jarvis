"""Helpers for matching a table of proper nouns (airline names, city names)
against free text, complementing `base.py`'s alias-driven `find_literal`,
which is keyed by canonical value instead of by the surface form itself.
"""


def find_value_by_longest_key(text: str, table: dict[str, str]) -> str | None:
    """Return the value of the longest `table` key found as a substring.

    Longest match wins so a specific name (e.g. "American Eagle") is never
    shadowed by a shorter one that happens to be its prefix (e.g. "American").
    """
    lowered = text.lower()
    matches = [(key, value) for key, value in table.items() if key.lower() in lowered]
    if not matches:
        return None
    return max(matches, key=lambda pair: len(pair[0]))[1]


def find_ordered_values(text: str, table: dict[str, str]) -> list[str]:
    """Return every matched `table` value, in the order its key reads in `text`.

    Used for phrases like "de Chicago a Los Ángeles", where the same table
    (airport codes) supplies both an origin and a destination and only word
    order tells them apart. Keys are tried longest-first so a short key that
    is a prefix of a longer one does not also match its span.
    """
    lowered = text.lower()
    occupied_spans: list[tuple[int, int]] = []
    found: list[tuple[int, str]] = []
    for key in sorted(table, key=len, reverse=True):
        index = lowered.find(key.lower())
        if index == -1 or _overlaps(index, len(key), occupied_spans):
            continue
        occupied_spans.append((index, index + len(key)))
        found.append((index, table[key]))
    return [value for _, value in sorted(found)]


def _overlaps(index: int, length: int, spans: list[tuple[int, int]]) -> bool:
    """Return whether `[index, index + length)` overlaps any span in `spans`."""
    end = index + length
    return any(index < span_end and end > span_start for span_start, span_end in spans)
