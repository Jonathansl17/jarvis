"""Calendar-phrase parsing shared by extractors that need a day-of-month or
a full ISO date out of Spanish text, built on a caller-supplied month-name
table (see `rules/tables/calendar.py`).
"""

import re
from datetime import date

_DAY_MONTH_PATTERN = r"\b(?P<day>\d{{1,2}})\s+de\s+(?:{alternation})\b"
_FULL_DATE_PATTERN = r"\b(?P<day>\d{{1,2}})\s+de\s+(?P<month>{alternation})\s+de\s+(?P<year>\d{{4}})\b"
_TODAY_KEYWORD = "hoy"


def find_day_of_month(text: str, month_names: dict[str, int]) -> int | None:
    """Return the day from a "<day> de <month name>" phrase, if present."""
    pattern = re.compile(_DAY_MONTH_PATTERN.format(alternation=_month_alternation(month_names)))
    match = pattern.search(text.lower())
    return int(match.group("day")) if match else None


def find_full_date(text: str, month_names: dict[str, int]) -> str | None:
    """Return an ISO "YYYY-MM-DD" date parsed from Spanish text, or None.

    Recognises a full "<day> de <month> de <year>" phrase, or the literal
    "hoy" for today's date.
    """
    lowered = text.lower()
    if _TODAY_KEYWORD in lowered:
        return date.today().isoformat()
    pattern = re.compile(_FULL_DATE_PATTERN.format(alternation=_month_alternation(month_names)))
    match = pattern.search(lowered)
    if not match:
        return None
    day = int(match.group("day"))
    month = month_names[match.group("month")]
    year = match.group("year")
    return f"{year}-{month:02d}-{day:02d}"


def _month_alternation(month_names: dict[str, int]) -> str:
    """Return `month_names`' keys as a regex alternation, longest name first."""
    return "|".join(re.escape(name) for name in sorted(month_names, key=len, reverse=True))
