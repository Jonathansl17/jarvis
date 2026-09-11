"""Spanish calendar vocabulary shared by extractors that read a date, a
weekday, or a time-of-day phrase out of free text.
"""

MONTH_NAMES: dict[str, int] = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11,
    "diciembre": 12,
}

WEEKDAY_NAMES: dict[str, int] = {
    "lunes": 1, "martes": 2, "miercoles": 3, "miércoles": 3, "jueves": 4,
    "viernes": 5, "sabado": 6, "sábado": 6, "domingo": 7,
}

# Canonical (English, internal-only) day-part keys, so the alias table can be
# read with `find_literal` and the offset table with a plain dict lookup.
DAY_PART_ALIASES: dict[str, tuple[str, ...]] = {
    "morning": ("de la manana", "de la mañana", "manana", "mañana"),
    "afternoon": ("de la tarde", "tarde"),
    "night": ("de la noche", "noche"),
}

# Added to a plain 12-hour clock number to get the 24-hour departure hour.
DAY_PART_HOUR_OFFSETS: dict[str, int] = {
    "morning": 0,
    "afternoon": 12,
    "night": 12,
}
