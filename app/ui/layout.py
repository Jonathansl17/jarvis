"""Builds the JarvisTEC window's grid: two columns of cards plus a status
strip, per §2-3 of the design spec. Pure Tk composition, no app behavior.
"""

import customtkinter as ctk

from app.ui import strings, theme
from app.ui.camera_render import VIDEO_HEIGHT_PX
from app.ui.layout_cards import build_camera_toggle_button, make_card
from app.ui.layout_types import WindowCallbacks, WindowStartupState, WindowWidgets
from app.ui.widgets.avatar_pane import AvatarPane
from app.ui.widgets.camera_preview import CameraPreview
from app.ui.widgets.conversation_view import ConversationView
from app.ui.widgets.input_row import InputRow
from app.ui.widgets.key_hints_bar import KeyHintsBar
from app.ui.widgets.status_bar import StatusBar

WINDOW_SIZE = "1280x800"
WINDOW_MIN_SIZE = (1100, 720)
_LEFT_COLUMN_WIDTH_PX = 400
WINDOW_PADDING_PX = 16
_COLUMN_GAP_PX = 16
_CARD_GAP_PX = 12
_CARD_PADDING_PX = 14

# The camera card is fixed-height (not grid-stretched, unlike the avatar
# card above it); its height is the sum of its own content, so it never
# leaves dead space below the video like a grid-stretched card would.
_CAMERA_CARD_HEADER_HEIGHT_PX = 44
_CAMERA_CARD_EMOTION_ROW_HEIGHT_PX = 34


def build_window(
    root: ctk.CTk, fonts: theme.Fonts, startup: WindowStartupState, callbacks: WindowCallbacks
) -> WindowWidgets:
    """Configure `root`'s chrome and grid once, returning every interactive widget.

    Sizing/position are set here only, at startup — never again on resize;
    the window manager and Tk's own geometry manager own everything after.
    """
    root.title(strings.WINDOW_TITLE)
    root.geometry(WINDOW_SIZE)
    root.minsize(*WINDOW_MIN_SIZE)
    root.configure(fg_color=theme.COLOR_BG_APP)
    root.grid_columnconfigure(0, weight=0)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=0)

    avatar_pane, camera_preview, camera_toggle_button = _build_left_column(root, fonts, startup, callbacks)
    conversation_view, input_row = _build_right_column(root, fonts, callbacks)
    status_bar = _build_bottom_bar(root, fonts, startup)
    return WindowWidgets(
        avatar_pane, camera_preview, camera_toggle_button, conversation_view, input_row, status_bar
    )


def _build_bottom_bar(root: ctk.CTk, fonts: theme.Fonts, startup: WindowStartupState) -> StatusBar:
    """Stack the key-hints row above the status strip, spanning both columns."""
    bottom = ctk.CTkFrame(root, fg_color="transparent")
    bottom.grid(row=1, column=0, columnspan=2, sticky="ew", padx=WINDOW_PADDING_PX, pady=(0, WINDOW_PADDING_PX))
    KeyHintsBar(bottom, fonts).pack(fill="x", pady=(0, 4))
    status_bar = StatusBar(bottom, startup.stt_engine_name, startup.initial_ia_state, fonts)
    status_bar.pack(fill="x")
    return status_bar


def _build_left_column(
    root: ctk.CTk, fonts: theme.Fonts, startup: WindowStartupState, callbacks: WindowCallbacks
) -> tuple[AvatarPane, CameraPreview, ctk.CTkButton]:
    """Build the fixed-width avatar and camera cards.

    `grid_propagate(False)` on this column, plus the avatar/camera images'
    own fixed pixel sizes, keep the incoming webcam/avatar frames from ever
    driving this layout's size — only the window/card chrome does.
    """
    column = ctk.CTkFrame(root, width=_LEFT_COLUMN_WIDTH_PX, fg_color="transparent")
    column.grid(row=0, column=0, sticky="ns", padx=(WINDOW_PADDING_PX, _COLUMN_GAP_PX // 2), pady=WINDOW_PADDING_PX)
    column.grid_propagate(False)
    column.grid_rowconfigure(0, weight=1)
    column.grid_rowconfigure(1, weight=0)

    avatar_card = make_card(column, fonts, strings.CARD_TITLE_AVATAR)
    avatar_card.grid(row=0, column=0, sticky="nsew")
    avatar_card.grid_propagate(False)
    avatar_pane = AvatarPane(avatar_card)
    avatar_pane.pack(expand=True)

    camera_toggle_button = None

    def _attach_toggle(header: ctk.CTkFrame) -> ctk.CTkButton:
        nonlocal camera_toggle_button
        camera_toggle_button = build_camera_toggle_button(
            header, fonts, startup.camera_enabled, callbacks.on_camera_toggle
        )
        return camera_toggle_button

    camera_card = make_card(column, fonts, strings.CARD_TITLE_CAMERA, right_widget_factory=_attach_toggle)
    camera_card.configure(height=_camera_card_height_px())
    camera_card.grid(row=1, column=0, sticky="ew", pady=(_CARD_GAP_PX, 0))
    camera_card.grid_propagate(False)
    camera_preview = CameraPreview(camera_card, fonts)
    camera_preview.pack()
    return avatar_pane, camera_preview, camera_toggle_button


def _camera_card_height_px() -> int:
    """The camera card's fixed height: header, video, emotion word, padding."""
    return (
        _CAMERA_CARD_HEADER_HEIGHT_PX
        + VIDEO_HEIGHT_PX
        + _CAMERA_CARD_EMOTION_ROW_HEIGHT_PX
        + _CARD_PADDING_PX
    )


def _build_right_column(
    root: ctk.CTk, fonts: theme.Fonts, callbacks: WindowCallbacks
) -> tuple[ConversationView, InputRow]:
    """Build the conversation card and the input row below it."""
    column = ctk.CTkFrame(root, fg_color="transparent")
    column.grid(row=0, column=1, sticky="nsew", padx=(_COLUMN_GAP_PX // 2, WINDOW_PADDING_PX), pady=WINDOW_PADDING_PX)
    column.grid_rowconfigure(0, weight=1)
    column.grid_columnconfigure(0, weight=1)

    conversation_card = make_card(column, fonts, strings.CARD_TITLE_CONVERSATION)
    conversation_card.grid(row=0, column=0, sticky="nsew")
    conversation_view = ConversationView(conversation_card, fonts)
    conversation_view.pack(fill="both", expand=True)

    input_row = InputRow(column, fonts, on_send=callbacks.on_send, on_mic_toggle=callbacks.on_mic_toggle)
    input_row.grid(row=1, column=0, sticky="ew", pady=(_CARD_GAP_PX, 0))
    return conversation_view, input_row
