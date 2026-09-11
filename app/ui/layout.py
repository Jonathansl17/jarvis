"""Builds the JarvisTEC window's grid: two columns of cards plus a status
strip, per §2-3 of the design spec. Pure Tk composition, no app behavior.
"""

from collections.abc import Callable

import customtkinter as ctk

from app.ui import strings, theme
from app.ui.layout_types import WindowCallbacks, WindowStartupState, WindowWidgets
from app.ui.widgets.avatar_pane import AvatarPane
from app.ui.widgets.camera_preview import CameraPreview
from app.ui.widgets.conversation_view import ConversationView
from app.ui.widgets.input_row import InputRow
from app.ui.widgets.key_hints_bar import KeyHintsBar
from app.ui.widgets.status_bar import StatusBar

WINDOW_SIZE = "1100x700"
WINDOW_MIN_SIZE = (1000, 650)
_LEFT_COLUMN_WIDTH_PX = 308
WINDOW_PADDING_PX = 16
_COLUMN_GAP_PX = 16
_CARD_GAP_PX = 12
_CARD_CORNER_RADIUS_PX = 12
_CARD_PADDING_PX = 14
_CAMERA_TOGGLE_SIZE_PX = (44, 22)


def build_window(
    root: ctk.CTk, fonts: theme.Fonts, status_info: StatusBarInfo, callbacks: WindowCallbacks
) -> WindowWidgets:
    """Configure `root`'s chrome and grid, returning every interactive widget."""
    root.title(strings.WINDOW_TITLE)
    root.geometry(WINDOW_SIZE)
    root.minsize(*WINDOW_MIN_SIZE)
    root.configure(fg_color=theme.COLOR_BG_APP)
    root.grid_columnconfigure(0, weight=0)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=0)

    avatar_pane, camera_preview, camera_toggle_button = _build_left_column(root, fonts, callbacks.on_camera_toggle)
    conversation_view, input_row = _build_right_column(root, fonts, callbacks)
    status_bar = _build_bottom_bar(root, fonts, status_info)
    return WindowWidgets(
        avatar_pane, camera_preview, camera_toggle_button, conversation_view, input_row, status_bar
    )


def _build_bottom_bar(root: ctk.CTk, fonts: theme.Fonts, status_info: StatusBarInfo) -> StatusBar:
    """Stack the key-hints row above the status strip, spanning both columns."""
    bottom = ctk.CTkFrame(root, fg_color="transparent")
    bottom.grid(row=1, column=0, columnspan=2, sticky="ew", padx=WINDOW_PADDING_PX, pady=(0, WINDOW_PADDING_PX))
    KeyHintsBar(bottom, fonts).pack(fill="x", pady=(0, 4))
    status_bar = StatusBar(bottom, status_info.stt_engine_name, status_info.initial_ia_state, fonts)
    status_bar.pack(fill="x")
    return status_bar


def _build_left_column(
    root: ctk.CTk, fonts: theme.Fonts, on_camera_toggle: Callable[[], None]
) -> tuple[AvatarPane, CameraPreview, ctk.CTkButton]:
    """Build the fixed-width avatar and camera cards."""
    column = ctk.CTkFrame(root, width=_LEFT_COLUMN_WIDTH_PX, fg_color="transparent")
    column.grid(row=0, column=0, sticky="ns", padx=(WINDOW_PADDING_PX, _COLUMN_GAP_PX // 2), pady=WINDOW_PADDING_PX)
    column.grid_propagate(False)
    column.grid_rowconfigure(1, weight=1)

    avatar_card = _make_card(column, fonts, strings.CARD_TITLE_AVATAR)
    avatar_card.grid(row=0, column=0, sticky="ew")
    avatar_pane = AvatarPane(avatar_card)
    avatar_pane.pack(pady=(0, _CARD_PADDING_PX // 2))

    camera_toggle_button = None

    def _attach_toggle(header: ctk.CTkFrame) -> ctk.CTkButton:
        nonlocal camera_toggle_button
        camera_toggle_button = _build_camera_toggle_button(header, fonts, on_camera_toggle)
        return camera_toggle_button

    camera_card = _make_card(column, fonts, strings.CARD_TITLE_CAMERA, right_widget_factory=_attach_toggle)
    camera_card.grid(row=1, column=0, sticky="nsew", pady=(_CARD_GAP_PX, 0))
    camera_preview = CameraPreview(camera_card, fonts)
    camera_preview.pack()
    return avatar_pane, camera_preview, camera_toggle_button


def _build_right_column(
    root: ctk.CTk, fonts: theme.Fonts, callbacks: WindowCallbacks
) -> tuple[ConversationView, InputRow]:
    """Build the conversation card and the input row below it."""
    column = ctk.CTkFrame(root, fg_color="transparent")
    column.grid(row=0, column=1, sticky="nsew", padx=(_COLUMN_GAP_PX // 2, WINDOW_PADDING_PX), pady=WINDOW_PADDING_PX)
    column.grid_rowconfigure(0, weight=1)
    column.grid_columnconfigure(0, weight=1)

    conversation_card = _make_card(column, fonts, strings.CARD_TITLE_CONVERSATION)
    conversation_card.grid(row=0, column=0, sticky="nsew")
    conversation_view = ConversationView(conversation_card, fonts)
    conversation_view.pack(fill="both", expand=True)

    input_row = InputRow(column, fonts, on_send=callbacks.on_send, on_mic_toggle=callbacks.on_mic_toggle)
    input_row.grid(row=1, column=0, sticky="ew", pady=(_CARD_GAP_PX, 0))
    return conversation_view, input_row


def _make_card(
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


def _build_camera_toggle_button(
    header: ctk.CTkFrame, fonts: theme.Fonts, on_camera_toggle: Callable[[], None]
) -> ctk.CTkButton:
    """A small ON/OFF button for mouse-only users to toggle the webcam (§15)."""
    width, height = _CAMERA_TOGGLE_SIZE_PX
    return ctk.CTkButton(
        header,
        text=strings.CAMERA_TOGGLE_ON,
        width=width,
        height=height,
        corner_radius=height // 2,
        font=fonts.body_small,
        fg_color=theme.COLOR_ACCENT_PRIMARY,
        text_color=theme.COLOR_BG_APP,
        command=on_camera_toggle,
    )
