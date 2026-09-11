"""Parameter/return-value bundles for `layout.build_window`, split out to
keep `layout.py` within the project's file-size limit.
"""

from collections.abc import Callable
from dataclasses import dataclass

import customtkinter as ctk

from app.ui.widgets.avatar_pane import AvatarPane
from app.ui.widgets.camera_preview import CameraPreview
from app.ui.widgets.conversation_view import ConversationView
from app.ui.widgets.input_row import InputRow
from app.ui.widgets.status_bar import StatusBar


@dataclass(frozen=True)
class WindowCallbacks:
    """User-action callbacks the window's widgets are wired to."""

    on_send: Callable[[], None]
    on_mic_toggle: Callable[[], None]
    on_camera_toggle: Callable[[], None]
    on_text_copied: Callable[[], None]


@dataclass(frozen=True)
class WindowStartupState:
    """Startup values the window's widgets need but never own themselves.

    `camera_enabled` seeds both the camera toggle button's initial label
    and whether `JarvisApp.run()` starts the worker — one value, one
    source of truth, so the button can never claim "ON" while the card
    shows disabled.
    """

    stt_engine_name: str
    initial_ia_state: str
    camera_enabled: bool


@dataclass(frozen=True)
class WindowWidgets:
    """Every widget `ui/app.py` needs a handle to after layout is built."""

    avatar_pane: AvatarPane
    camera_preview: CameraPreview
    camera_toggle_button: ctk.CTkButton
    conversation_view: ConversationView
    input_row: InputRow
    status_bar: StatusBar
