"""Extracts flight_delay_regression fields from Spanish free text."""

from typing import Any, ClassVar

from app.intents.rules.base import find_from_table, find_number_near, find_value_after

_MONTH_NAMES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11,
    "diciembre": 12,
}
_WEEKDAY_NAMES = {
    "lunes": 1, "martes": 2, "miercoles": 3, "miércoles": 3, "jueves": 4,
    "viernes": 5, "sabado": 6, "sábado": 6, "domingo": 7,
}

_DAY_OF_MONTH_KEYWORDS = ("dia", "día")
_HOUR_KEYWORDS = ("hora de salida", "hora", "a las")
_DISTANCE_KEYWORDS = ("millas", "distancia")
_CARRIER_KEYWORDS = ("aerolinea", "aerolínea")
_ORIGIN_KEYWORDS = ("desde", "origen")
_DEST_KEYWORDS = ("hasta", "destino")


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
        month = find_from_table(text, _MONTH_NAMES)
        if month is not None:
            fields["month"] = month
        weekday = find_from_table(text, _WEEKDAY_NAMES)
        if weekday is not None:
            fields["day_of_week"] = weekday
        day_of_month = find_number_near(text, _DAY_OF_MONTH_KEYWORDS)
        if day_of_month is not None:
            fields["day_of_month"] = int(day_of_month)
        hour = find_number_near(text, _HOUR_KEYWORDS)
        if hour is not None:
            fields["dep_hour"] = int(hour)

    @staticmethod
    def _add_route(text: str, fields: dict[str, Any]) -> None:
        carrier = find_value_after(text, _CARRIER_KEYWORDS)
        if carrier is not None:
            fields["carrier"] = carrier
        origin = find_value_after(text, _ORIGIN_KEYWORDS)
        if origin is not None:
            fields["origin"] = origin
        dest = find_value_after(text, _DEST_KEYWORDS)
        if dest is not None:
            fields["dest"] = dest
        distance = find_number_near(text, _DISTANCE_KEYWORDS)
        if distance is not None:
            fields["distance"] = distance
