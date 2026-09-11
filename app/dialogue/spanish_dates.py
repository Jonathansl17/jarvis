"""Spanish month names, used only to render a forecast date as prose."""

from datetime import date

_MONTH_NAMES: dict[int, str] = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
    7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre",
    12: "diciembre",
}
_SPANISH_DATE_TEMPLATE = "{day} de {month} de {year}"


def format_spanish_date(iso_date: str) -> str:
    """Render an ISO date string as Spanish prose, e.g. '1 de agosto de 2017'."""
    parsed = date.fromisoformat(iso_date)
    return _SPANISH_DATE_TEMPLATE.format(day=parsed.day, month=_MONTH_NAMES[parsed.month], year=parsed.year)
