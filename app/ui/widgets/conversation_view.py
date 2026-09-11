"""Shows the turn-by-turn transcript (§10 of the design spec)."""

from collections.abc import Callable
from datetime import datetime

import customtkinter as ctk

from app.intents.models import Speaker
from app.ui import strings, theme
from app.ui.theme import Fonts

_TIMESTAMP_FORMAT = "%H:%M:%S"
_BUBBLE_CORNER_RADIUS_PX = 12
_BUBBLE_WRAP_FRACTION = 0.70
_BUBBLE_PADDING_PX = (14, 10)
_TURN_GAP_PX = 14
_FALLBACK_WIDTH_PX = 700  # Used only before the first layout pass reports a real width.


class ConversationView(ctk.CTkScrollableFrame):
    """Appends one labeled, timestamped bubble per turn, auto-scrolling down."""

    def __init__(
        self, master: ctk.CTkBaseClass, fonts: Fonts, on_copied: Callable[[], None] | None = None, **kwargs: object
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._fonts = fonts
        self._on_copied = on_copied
        self._bubbles: list[ctk.CTkLabel] = []
        self._last_width = 0
        self._resize_job: str | None = None
        # Bound only on this container (never `bind_all`); re-wrapping a
        # bubble changes its *height*, not this frame's width, so guarding
        # on width and debouncing via `after_idle` stops that from ever
        # re-triggering itself — see the resize-loop regression this fixes.
        self.bind("<Configure>", self._on_resize)

    def append_turn(self, speaker: Speaker, text: str) -> None:
        """Append one row for `speaker`, then scroll to the newest turn."""
        if speaker is Speaker.SYSTEM:
            self._append_system_row(text)
        else:
            self._append_bubble_row(speaker, text)
        self.after_idle(self._scroll_to_bottom)

    def _scroll_to_bottom(self) -> None:
        """Refresh the scroll region once the new row is laid out, then jump to it."""
        self.update_idletasks()
        canvas = self._parent_canvas
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.yview_moveto(1.0)

    def _append_system_row(self, text: str) -> None:
        """A centered, muted line with no bubble or sender label."""
        row = ctk.CTkLabel(self, text=text, font=self._fonts.body_small, text_color=theme.COLOR_SYSTEM_TEXT)
        row.pack(fill="x", pady=(_TURN_GAP_PX, 0))

    def _append_bubble_row(self, speaker: Speaker, text: str) -> None:
        """A sender label, bubble, and timestamp, aligned per §10's rules."""
        is_user = speaker is Speaker.USER
        anchor = "e" if is_user else "w"
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", pady=(_TURN_GAP_PX, 0))

        label_text = strings.SENDER_USER if is_user else strings.SENDER_ASSISTANT
        label_color = theme.COLOR_TEXT_PRIMARY if is_user else theme.COLOR_ACCENT_PRIMARY
        ctk.CTkLabel(row, text=label_text, font=self._fonts.label, text_color=label_color).pack(anchor=anchor)

        bubble = ctk.CTkLabel(
            row,
            text=text,
            font=self._fonts.body,
            text_color=theme.COLOR_TEXT_PRIMARY,
            fg_color=theme.COLOR_BUBBLE_USER_BG if is_user else theme.COLOR_BUBBLE_ASSISTANT_BG,
            corner_radius=_BUBBLE_CORNER_RADIUS_PX,
            wraplength=self._bubble_wrap_px(),
            justify="left",
            padx=_BUBBLE_PADDING_PX[0],
            pady=_BUBBLE_PADDING_PX[1],
        )
        bubble.pack(anchor=anchor)
        bubble.bind("<Button-3>", lambda _event, value=text: self._copy_to_clipboard(value))
        bubble.bind("<Double-Button-1>", lambda _event, value=text: self._copy_to_clipboard(value))
        self._bubbles.append(bubble)

        timestamp = datetime.now().strftime(_TIMESTAMP_FORMAT)
        ctk.CTkLabel(row, text=timestamp, font=self._fonts.body_small, text_color=theme.COLOR_TEXT_MUTED).pack(
            anchor=anchor
        )

    def _copy_to_clipboard(self, text: str) -> None:
        """Right click or double click on a bubble copies its whole text."""
        self.clipboard_clear()
        self.clipboard_append(text)
        if self._on_copied is not None:
            self._on_copied()

    def _on_resize(self, event: object) -> None:
        """Debounce a real width change into one wraplength pass on idle."""
        width = event.width
        if width == self._last_width:
            return
        self._last_width = width
        if self._resize_job is not None:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after_idle(self._apply_wrap, width)

    def _apply_wrap(self, width: int) -> None:
        """Recompute every bubble's wraplength for `width`, once per idle cycle."""
        self._resize_job = None
        wrap_px = max(1, round(width * _BUBBLE_WRAP_FRACTION))
        for bubble in self._bubbles:
            bubble.configure(wraplength=wrap_px)

    def _bubble_wrap_px(self) -> int:
        """Max bubble text width: 70% of the conversation column's current width."""
        width = self.winfo_width()
        if width <= 1:
            width = _FALLBACK_WIDTH_PX
        return max(1, round(width * _BUBBLE_WRAP_FRACTION))
