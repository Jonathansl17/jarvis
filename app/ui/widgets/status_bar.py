"""Shows the status strip: MIC/EMO/API/STT/IA segments plus a transient
error line (§13 of the design spec, extended with an IA field — system
notices and background errors surface here, never as chat lines). The key
hints live in the separate `KeyHintsBar` row above this one.

The EMO field always shows the exact same text as the camera card's
emotion word (`ui.emotion_label.format_emotion_reading`); there is no
separate "uncertain" wording here — the confidence cutoff only decides
whether the avatar mirrors an emotion, never what either label says.
"""

import customtkinter as ctk

from app.emotion.protocol import Emotion
from app.ui import strings, theme
from app.ui.emotion_label import format_emotion_reading
from app.ui.theme import Fonts

_STRIP_HEIGHT_PX = 32
_DOT_SIZE_PX = 8
_SEGMENT_PADDING_PX = 10
_DOT_PADDING_PX = 6

MIC_IDLE = strings.STATUS_MIC_IDLE
MIC_RECORDING = strings.STATUS_MIC_RECORDING
MIC_OFF = strings.STATUS_MIC_OFF

API_CONNECTED = strings.STATUS_API_CONNECTED
API_ERROR = strings.STATUS_API_ERROR
API_BUSY = strings.STATUS_API_BUSY

_SUCCESS_STATES = {MIC_IDLE, API_CONNECTED}
_WARNING_STATES = {API_BUSY}
_DANGER_STATES = {MIC_RECORDING, MIC_OFF, API_ERROR}


class StatusBar(ctk.CTkFrame):
    """Fixed status segments on the left, a transient error line on the right."""

    def __init__(
        self, master: ctk.CTkBaseClass, stt_engine_name: str, initial_ia_state: str, fonts: Fonts, **kwargs: object
    ) -> None:
        super().__init__(master, height=_STRIP_HEIGHT_PX, fg_color=theme.COLOR_BG_CARD, **kwargs)
        self._fonts = fonts
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        segments = ctk.CTkFrame(self, fg_color="transparent")
        segments.grid(row=0, column=0, sticky="w", padx=(_SEGMENT_PADDING_PX, 0))
        segments.grid_columnconfigure((0, 1, 2, 3, 4), weight=0)
        self._mic_dot, self._mic_text = self._build_segment(segments, 0, "MIC")
        self._emo_dot, self._emo_text = self._build_segment(segments, 1, "EMO")
        self._api_dot, self._api_text = self._build_segment(segments, 2, "API")
        self._stt_dot, self._stt_text = self._build_segment(segments, 3, "STT")
        self._ia_dot, self._ia_text = self._build_segment(segments, 4, "IA")

        self._error_label = ctk.CTkLabel(self, text="", font=fonts.status, text_color=theme.COLOR_DANGER)
        self._error_label.grid(row=0, column=1, sticky="e", padx=_SEGMENT_PADDING_PX)

        self.set_mic_state(MIC_IDLE)
        self.set_camera_disabled()
        self.set_api_state(API_CONNECTED)
        self.set_ia_state(initial_ia_state)
        self.set_stt_engine(stt_engine_name)

    def set_stt_engine(self, engine_name: str) -> None:
        """Show the loaded speech-to-text engine as active."""
        self._stt_text.configure(text=engine_name)
        self._stt_dot.configure(fg_color=theme.COLOR_SUCCESS)

    def set_mic_state(self, state: str) -> None:
        """Update the MIC field to `state` (en reposo, grabando, or apagado)."""
        self._mic_text.configure(text=state)
        self._mic_dot.configure(fg_color=_dot_color(state))

    def set_emotion_reading(self, reading: tuple[Emotion, float] | None) -> None:
        """Show the same text the camera card shows for `reading` (or no face)."""
        self._emo_text.configure(text=format_emotion_reading(reading))
        dot_color = theme.COLOR_SUCCESS if reading is not None else theme.COLOR_ACCENT_SECONDARY
        self._emo_dot.configure(fg_color=dot_color)

    def set_camera_disabled(self) -> None:
        """Show that the webcam emotion sampler is turned off."""
        self._emo_text.configure(text=strings.CAMERA_DISABLED_LABEL)
        self._emo_dot.configure(fg_color=theme.COLOR_DANGER)

    def set_api_state(self, state: str) -> None:
        """Update the API field to `state` (conectada, ocupada, or error)."""
        self._api_text.configure(text=state)
        self._api_dot.configure(fg_color=_dot_color(state))

    def set_ia_state(self, label: str) -> None:
        """Update the IA field to the active model name, or "reglas"."""
        self._ia_text.configure(text=label)
        self._ia_dot.configure(fg_color=theme.COLOR_SUCCESS)

    def set_error(self, detail: str) -> None:
        """Show a background failure as a short red line, replacing any prior one."""
        self._error_label.configure(text=detail)

    def _build_segment(self, master: ctk.CTkBaseClass, column: int, label: str) -> tuple[ctk.CTkFrame, ctk.CTkLabel]:
        """Build one `label ● state` segment and return its dot and state label."""
        segment = ctk.CTkFrame(master, fg_color="transparent")
        segment.grid(row=0, column=column, sticky="w", padx=(0, _SEGMENT_PADDING_PX))
        ctk.CTkLabel(segment, text=label, font=self._fonts.status, text_color=theme.COLOR_TEXT_MUTED).pack(
            side="left"
        )
        dot = ctk.CTkFrame(
            segment, width=_DOT_SIZE_PX, height=_DOT_SIZE_PX, corner_radius=_DOT_SIZE_PX // 2
        )
        dot.pack(side="left", padx=_DOT_PADDING_PX)
        state_label = ctk.CTkLabel(segment, text="", font=self._fonts.status, text_color=theme.COLOR_TEXT_PRIMARY)
        state_label.pack(side="left")
        return dot, state_label


def _dot_color(state: str) -> str:
    """Map a status word to its dot color, per §13's fixed color table."""
    if state in _SUCCESS_STATES:
        return theme.COLOR_SUCCESS
    if state in _WARNING_STATES:
        return theme.COLOR_ACCENT_SECONDARY
    if state in _DANGER_STATES:
        return theme.COLOR_DANGER
    return theme.COLOR_SUCCESS
