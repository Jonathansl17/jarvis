"""CustomTkinter dark palette and font resolution, from `gui-design.md` §4-5.

Dark mode only — the design spec is single-theme by design (§4), so there
is no light-mode branch to maintain here.
"""

import platform
import tkinter.font as tkfont
from dataclasses import dataclass

import customtkinter as ctk

# §4 color tokens, named exactly as the design spec's tokens.
COLOR_BG_APP = "#0F1115"
COLOR_BG_CARD = "#171A21"
COLOR_BG_CARD_ELEVATED = "#1C212B"
COLOR_BORDER_SUBTLE = "#262B36"
COLOR_BORDER_STRONG = "#3A4152"
COLOR_TEXT_PRIMARY = "#E8EDF2"
COLOR_TEXT_SECONDARY = "#A9B4C4"
COLOR_TEXT_MUTED = "#6B7480"
COLOR_ACCENT_PRIMARY = "#2DE2C9"
COLOR_ACCENT_SECONDARY = "#F5A623"
COLOR_DANGER = "#FF4D4F"
COLOR_SUCCESS = "#34D399"
COLOR_BUBBLE_USER_BG = "#17332F"
COLOR_BUBBLE_ASSISTANT_BG = "#1B1F29"
COLOR_BUBBLE_ASSISTANT_BORDER = "#3A4152"
COLOR_SYSTEM_TEXT = "#6B7480"

# §8 per-emotion camera label colors.
EMOTION_LABEL_COLORS = {
    "happy": "#34D399",
    "sad": "#5B8DEF",
    "angry": "#FF4D4F",
    "surprise": "#F5A623",
    "fear": "#B58BFF",
    "disgust": "#8AA624",
    "neutral": COLOR_TEXT_SECONDARY,
}

_SANS_FALLBACKS = ("Noto Sans", "DejaVu Sans")
_MONO_FALLBACK_LINUX = "DejaVu Sans Mono"
_MONO_FALLBACK_OTHER = "Courier New"
_DEFAULT_SANS = "Helvetica"


@dataclass(frozen=True)
class Fonts:
    """The named font roles from §5's typography table."""

    title: ctk.CTkFont
    card_title: ctk.CTkFont
    body: ctk.CTkFont
    body_small: ctk.CTkFont
    label: ctk.CTkFont
    emotion_word: ctk.CTkFont
    status: ctk.CTkFont
    entry: ctk.CTkFont


def apply_theme() -> Fonts:
    """Set the dark appearance mode and resolve this platform's font roles."""
    ctk.set_appearance_mode("dark")
    sans, mono = _resolve_sans_family(), _resolve_mono_family()
    return Fonts(
        title=ctk.CTkFont(family=sans, size=20, weight="bold"),
        card_title=ctk.CTkFont(family=sans, size=14, weight="bold"),
        body=ctk.CTkFont(family=sans, size=14, weight="normal"),
        body_small=ctk.CTkFont(family=sans, size=12, weight="normal"),
        label=ctk.CTkFont(family=sans, size=12, weight="bold"),
        emotion_word=ctk.CTkFont(family=sans, size=14, weight="bold"),
        status=ctk.CTkFont(family=mono, size=11, weight="normal"),
        entry=ctk.CTkFont(family=sans, size=14, weight="normal"),
    )


def _resolve_sans_family() -> str:
    """Resolve the sans-serif family, per §5's Tk-has-no-CSS-fallbacks note."""
    if platform.system() == "Windows":
        return "Segoe UI"
    available = set(tkfont.families())
    for candidate in _SANS_FALLBACKS:
        if candidate in available:
            return candidate
    return _DEFAULT_SANS


def _resolve_mono_family() -> str:
    """Resolve the monospace family used by the status strip."""
    if platform.system() == "Windows":
        return "Cascadia Mono"
    available = set(tkfont.families())
    if _MONO_FALLBACK_LINUX in available:
        return _MONO_FALLBACK_LINUX
    return _MONO_FALLBACK_OTHER
