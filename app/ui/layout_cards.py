"""Titled-card chrome shared by every card in the window, split out of
`layout.py` to keep it within the project's file-size limit.
"""

from collections.abc import Callable

import customtkinter as ctk

from app.ui import strings, theme

_CARD_CORNER_RADIUS_PX = 12
_CARD_PADDING_PX = 14
_CAMERA_TOGGLE_SIZE_PX = (44, 22)


def make_card(
    master: ctk.CTkBaseClass,
    fonts: theme.Fonts,
    title: str,
    right_widget_factory: Callable[[ctk.CTkFrame], ctk.CTkBaseClass] | None = None,
) -> ctk.CTkFrame:
    """Build one titled card frame: rounded, padded, with its header packed."""
    card = ctk.CTkFrame(master, fg_color=theme.COLOR_BG_CARD, corner_radius=_CARD_CORNER_RADIUS_PX)
    header = ctk.CTkFrame(card, fg_color="transparent")
    header.pack(fill="x", padx=_CARD_PADDING_PX, pady=(_CARD_PADDING_PX, _CARD_PADDING_PX // 2))
    ctk.CTkLabel(header, text=title, font=fonts.card_title, text_color=theme.COLOR_TEXT_PRIMARY).pack(side="left")
    if right_widget_factory is not None:
        right_widget_factory(header).pack(side="right")
    return card


def build_camera_toggle_button(
    header: ctk.CTkFrame, fonts: theme.Fonts, camera_enabled: bool, on_camera_toggle: Callable[[], None]
) -> ctk.CTkButton:
    """A small ON/OFF button for mouse-only users to toggle the webcam (§15).

    Its initial label matches `camera_enabled` — the same flag `run()` uses
    to decide whether to start the worker — so the button is never wrong
    about the state it claims to control.
    """
    width, height = _CAMERA_TOGGLE_SIZE_PX
    label = strings.CAMERA_TOGGLE_ON if camera_enabled else strings.CAMERA_TOGGLE_OFF
    return ctk.CTkButton(
        header,
        text=label,
        width=width,
        height=height,
        corner_radius=height // 2,
        font=fonts.body_small,
        fg_color=theme.COLOR_ACCENT_PRIMARY,
        text_color=theme.COLOR_BG_APP,
        command=on_camera_toggle,
    )
