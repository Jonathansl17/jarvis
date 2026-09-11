"""Extracts flight_delay_regression fields from Spanish free text."""

from typing import Any, ClassVar

from app.intents.airline_codes import AIRPORT_CODES, CARRIER_CODES
from app.intents.rules.base import find_from_table, find_literal, find_number_near
from app.intents.rules.dates import find_day_of_month
from app.intents.rules.lookup import find_ordered_values, find_value_by_longest_key
from app.intents.rules.tables.calendar import (
    DAY_PART_ALIASES,
    DAY_PART_HOUR_OFFSETS,
    MONTH_NAMES,
    WEEKDAY_NAMES,
)

_HOUR_KEYWORDS = ("hora de salida", "hora", "a las")
_DISTANCE_KEYWORDS = ("millas", "distancia")
_NOON_HOUR = 12


class FlightDelayRegressionExtractor:
    """Extracts a scheduled flight's calendar slot, route, and distance."""

    required_fields: ClassVar[list[str]] = [
        "month", "day_of_month", "day_of_week", "dep_hour",
        "carrier", "origin", "dest", "distance",
    ]

    def extract(self, text: str) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        self._add_calendar(text, fields)
        self._add_route(text, fields)
        return fields

    @staticmethod
    def _add_calendar(text: str, fields: dict[str, Any]) -> None:
        month = find_from_table(text, MONTH_NAMES)
        if month is not None:
            fields["month"] = month
        weekday = find_from_table(text, WEEKDAY_NAMES)
        if weekday is not None:
            fields["day_of_week"] = weekday
        day_of_month = find_day_of_month(text, MONTH_NAMES)
        if day_of_month is not None:
            fields["day_of_month"] = day_of_month
        hour = _find_departure_hour(text)
        if hour is not None:
            fields["dep_hour"] = hour

    @staticmethod
    def _add_route(text: str, fields: dict[str, Any]) -> None:
        carrier = find_value_by_longest_key(text, CARRIER_CODES)
        if carrier is not None:
            fields["carrier"] = carrier
        airports = find_ordered_values(text, AIRPORT_CODES)
        if airports:
            fields["origin"] = airports[0]
        if len(airports) > 1:
            fields["dest"] = airports[1]
        distance = find_number_near(text, _DISTANCE_KEYWORDS)
        if distance is not None:
            fields["distance"] = distance


def _find_departure_hour(text: str) -> int | None:
    """Return the 24-hour departure hour from a "a las <n> de la <period>" phrase."""
    hour = find_number_near(text, _HOUR_KEYWORDS)
    if hour is None:
        return None
    hour = int(hour)
    period = find_literal(text, DAY_PART_ALIASES)
    offset = DAY_PART_HOUR_OFFSETS.get(period, 0)
    return hour + offset if hour < _NOON_HOUR else hour
