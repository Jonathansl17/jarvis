"""A slim, full-width row of key-binding hints shown above the status strip.

Split out of `status_bar.py`: fitting the hints text on the same row as the
MIC/EMO/API/STT/IA segments left too little room for either on narrower
windows, per the design spec's own instruction to keep the HUD readable.
"""

import customtkinter as ctk

from app.ui import theme
from app.ui.key_bindings import KEY_HINTS_TEXT
from app.ui.theme import Fonts

_HEIGHT_PX = 20


class KeyHintsBar(ctk.CTkLabel):
    """A single centered, muted line naming every global key binding."""

    def __init__(self, master: ctk.CTkBaseClass, fonts: Fonts, **kwargs: object) -> None:
        super().__init__(
            master,
            text=KEY_HINTS_TEXT,
            font=fonts.status,
            text_color=theme.COLOR_TEXT_MUTED,
            height=_HEIGHT_PX,
            **kwargs,
        )
