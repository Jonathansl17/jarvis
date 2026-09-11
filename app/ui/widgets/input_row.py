"""The entry plus one context-sensitive action button.

The button is the microphone while the entry is empty, the send arrow once
the user has typed something, and the recording indicator while the mic is
open, during which the entry is hidden. The glyphs are plain text: an emoji
mic rendered as a missing-glyph box on this font, and combining `image=`
with empty button text disables this CTk version's rounded corner mask.
"""

from collections.abc import Callable

import customtkinter as ctk

from app.ui import strings, theme
from app.ui.theme import Fonts

_ENTRY_HEIGHT_PX = 52
_ROW_PADDING_PX = 8
_ROW_HEIGHT_PX = _ENTRY_HEIGHT_PX + 2 * _ROW_PADDING_PX
_ROW_CORNER_RADIUS_PX = 10
_BUTTON_SIZE_PX = (96, 56)
_BUTTON_GAP_PX = 12
_IDLE_BORDER_WIDTH_PX = 2

_PULSE_PERIOD_MS = 800
_PULSE_BORDER_WIDTHS = (2, 4)


class InputRow(ctk.CTkFrame):
    """Text entry plus a single button that records or sends, via injected callbacks."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        fonts: Fonts,
        on_send: Callable[[], None],
        on_mic_toggle: Callable[[], None],
        **kwargs: object,
    ) -> None:
        super().__init__(
            master, height=_ROW_HEIGHT_PX, fg_color=theme.COLOR_BG_CARD_ELEVATED, corner_radius=_ROW_CORNER_RADIUS_PX, **kwargs
        )
        self._on_send = on_send
        self._on_mic_toggle = on_mic_toggle
        self._recording = False
        self._pulse_job: str | None = None
        self._pulse_phase = 0

        self.entry = ctk.CTkEntry(
            self, placeholder_text=strings.ENTRY_PLACEHOLDER, font=fonts.entry, height=_ENTRY_HEIGHT_PX
        )
        self.entry.bind("<Return>", lambda _event: on_send())
        self.entry.bind("<KeyRelease>", lambda _event: self._refresh_button())

        width, height = _BUTTON_SIZE_PX
        self.action_button = ctk.CTkButton(
            self, font=fonts.button, width=width, height=height, corner_radius=height // 2, command=self._on_press
        )
        self.action_button.pack(side="right", padx=(0, _ROW_PADDING_PX), pady=_ROW_PADDING_PX)
        self._show_entry()
        self._show_mic_idle()

    def get_text(self) -> str:
        """Return the entry's current text, unmodified."""
        return self.entry.get()

    def clear(self) -> None:
        """Empty the entry field and return the button to the microphone."""
        self.entry.delete(0, "end")
        self._refresh_button()

    def set_input_enabled(self, enabled: bool) -> None:
        """Enable or disable typing, e.g. while a recording is transcribing."""
        self.entry.configure(state="normal" if enabled else "disabled")

    def set_mic_recording(self, recording: bool) -> None:
        """Enter or leave the recording state: red pulsing button, entry hidden."""
        self._recording = recording
        self._stop_pulse()
        if recording:
            self._hide_entry()
            self.action_button.configure(
                fg_color=theme.COLOR_DANGER, text_color="white", text=strings.MIC_BUTTON_RECORDING
            )
            self._start_pulse()
        else:
            self._show_entry()
            self._refresh_button()

    def set_mic_processing(self) -> None:
        """Show the static processing state while the recording is transcribed."""
        self._recording = False
        self._stop_pulse()
        self.action_button.configure(
            fg_color=theme.COLOR_ACCENT_SECONDARY,
            border_color=theme.COLOR_ACCENT_SECONDARY,
            text_color=theme.COLOR_BG_APP,
            text=strings.MIC_BUTTON_PROCESSING,
        )

    def set_mic_disabled(self) -> None:
        """Dim the button when the microphone is unavailable."""
        self._stop_pulse()
        self.action_button.configure(fg_color="transparent", border_width=0, text=strings.MIC_BUTTON_IDLE)

    def _on_press(self) -> None:
        """Send when there is text, otherwise toggle the microphone."""
        if not self._recording and self.entry.get().strip():
            self._on_send()
        else:
            self._on_mic_toggle()

    def _refresh_button(self) -> None:
        """Pick the mic or the send look from whether the entry holds text."""
        if self._recording:
            return
        if self.entry.get().strip():
            self._show_send()
        else:
            self._show_mic_idle()

    def _show_mic_idle(self) -> None:
        self.action_button.configure(
            text=strings.MIC_BUTTON_IDLE,
            fg_color="transparent",
            text_color=theme.COLOR_ACCENT_PRIMARY,
            border_width=_IDLE_BORDER_WIDTH_PX,
            border_color=theme.COLOR_ACCENT_PRIMARY,
        )

    def _show_send(self) -> None:
        self.action_button.configure(
            text=strings.SEND_BUTTON,
            fg_color=theme.COLOR_ACCENT_PRIMARY,
            text_color=theme.COLOR_BG_APP,
            border_width=0,
        )

    def _show_entry(self) -> None:
        self.entry.pack(side="left", fill="x", expand=True, padx=(_ROW_PADDING_PX, _BUTTON_GAP_PX), pady=_ROW_PADDING_PX)

    def _hide_entry(self) -> None:
        self.entry.pack_forget()

    def _start_pulse(self) -> None:
        """Approximate the recording ring's pulse by oscillating border width."""
        self._pulse_phase = 0
        self._pulse_tick()

    def _pulse_tick(self) -> None:
        width = _PULSE_BORDER_WIDTHS[self._pulse_phase % len(_PULSE_BORDER_WIDTHS)]
        self.action_button.configure(border_width=width, border_color=theme.COLOR_DANGER)
        self._pulse_phase += 1
        self._pulse_job = self.after(_PULSE_PERIOD_MS // 2, self._pulse_tick)

    def _stop_pulse(self) -> None:
        if self._pulse_job is not None:
            self.after_cancel(self._pulse_job)
            self._pulse_job = None
