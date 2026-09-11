"""The entry, mic, and send controls, per §11-12 of the design spec.

Mic/send glyphs are plain text (`strings.MIC_BUTTON_*`, `SEND_BUTTON`)
rather than emoji or a rendered `CTkImage`: an emoji mic glyph rendered as
a missing-glyph box on this font, and — separately — combining `image=`
with empty button text was found to disable this CTk version's rounded
corner mask. Plain text avoids both.
"""

from collections.abc import Callable

import customtkinter as ctk

from app.ui import strings, theme
from app.ui.theme import Fonts

_ENTRY_HEIGHT_PX = 52
_ROW_PADDING_PX = 8
_ROW_HEIGHT_PX = _ENTRY_HEIGHT_PX + 2 * _ROW_PADDING_PX
_ROW_CORNER_RADIUS_PX = 10
_MIC_BUTTON_SIZE_PX = (96, 56)
_SEND_BUTTON_SIZE_PX = (56, 56)
_BUTTON_GAP_PX = 12

_PULSE_PERIOD_MS = 800
_PULSE_BORDER_WIDTHS = (2, 4)


class InputRow(ctk.CTkFrame):
    """Text entry plus mic-toggle and send buttons, wired via injected callbacks."""

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
        self._fonts = fonts
        self._pulse_job: str | None = None
        self._pulse_phase = 0

        self.entry = ctk.CTkEntry(
            self, placeholder_text=strings.ENTRY_PLACEHOLDER, font=fonts.entry, height=_ENTRY_HEIGHT_PX
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(_ROW_PADDING_PX, _BUTTON_GAP_PX), pady=_ROW_PADDING_PX)
        self.entry.bind("<Return>", lambda _event: on_send())

        mic_width, mic_height = _MIC_BUTTON_SIZE_PX
        self.mic_button = ctk.CTkButton(
            self,
            text=strings.MIC_BUTTON_IDLE,
            font=fonts.button,
            width=mic_width,
            height=mic_height,
            corner_radius=mic_height // 2,
            fg_color="transparent",
            text_color=theme.COLOR_ACCENT_PRIMARY,
            border_width=2,
            border_color=theme.COLOR_ACCENT_PRIMARY,
            command=on_mic_toggle,
        )
        self.mic_button.pack(side="left", padx=(0, _BUTTON_GAP_PX), pady=_ROW_PADDING_PX)

        send_width, send_height = _SEND_BUTTON_SIZE_PX
        self.send_button = ctk.CTkButton(
            self,
            text=strings.SEND_BUTTON,
            font=fonts.button,
            width=send_width,
            height=send_height,
            corner_radius=send_height // 2,
            fg_color=theme.COLOR_ACCENT_PRIMARY,
            text_color=theme.COLOR_BG_APP,
            command=on_send,
        )
        self.send_button.pack(side="left", padx=(0, _ROW_PADDING_PX), pady=_ROW_PADDING_PX)

    def get_text(self) -> str:
        """Return the entry's current text, unmodified."""
        return self.entry.get()

    def clear(self) -> None:
        """Empty the entry field."""
        self.entry.delete(0, "end")

    def set_input_enabled(self, enabled: bool) -> None:
        """Enable or disable typing, e.g. while a recording is transcribing."""
        self.entry.configure(state="normal" if enabled else "disabled")

    def set_mic_recording(self, recording: bool) -> None:
        """Switch the mic button between idle and recording (§12)."""
        self._stop_pulse()
        if recording:
            self.mic_button.configure(
                fg_color=theme.COLOR_DANGER, text_color="white", text=strings.MIC_BUTTON_RECORDING
            )
            self._start_pulse()
        else:
            self.mic_button.configure(
                fg_color="transparent", text_color=theme.COLOR_ACCENT_PRIMARY, text=strings.MIC_BUTTON_IDLE
            )

    def set_mic_processing(self) -> None:
        """Switch the mic button to its static processing state (§12)."""
        self._stop_pulse()
        self.mic_button.configure(
            fg_color=theme.COLOR_ACCENT_SECONDARY,
            border_color=theme.COLOR_ACCENT_SECONDARY,
            text_color=theme.COLOR_BG_APP,
            text=strings.MIC_BUTTON_PROCESSING,
        )

    def set_mic_disabled(self) -> None:
        """Dim the mic button when the microphone is unavailable (§12)."""
        self._stop_pulse()
        self.mic_button.configure(fg_color="transparent", border_width=0, text=strings.MIC_BUTTON_IDLE)

    def _start_pulse(self) -> None:
        """Approximate the recording ring's pulse by oscillating border width."""
        self._pulse_phase = 0
        self._pulse_tick()

    def _pulse_tick(self) -> None:
        width = _PULSE_BORDER_WIDTHS[self._pulse_phase % len(_PULSE_BORDER_WIDTHS)]
        self.mic_button.configure(border_width=width, border_color=theme.COLOR_DANGER)
        self._pulse_phase += 1
        self._pulse_job = self.after(_PULSE_PERIOD_MS // 2, self._pulse_tick)

    def _stop_pulse(self) -> None:
        if self._pulse_job is not None:
            self.after_cancel(self._pulse_job)
            self._pulse_job = None
        self.mic_button.configure(border_width=2, border_color=theme.COLOR_ACCENT_PRIMARY)
