"""Generic Spanish yes/no phrase table, shared by any extractor whose field
is a literal "Yes"/"No" value.
"""

YES_NO_ALIASES: dict[str, tuple[str, ...]] = {"Yes": ("si", "sí"), "No": ("no",)}
