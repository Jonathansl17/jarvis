"""Single source of truth for `JarvisApp`'s global key bindings, per §15.

`Enter` is bound directly on the entry widget (`widgets/input_row.py`)
since it only fires while that widget has focus; every binding here is
global (bound on the root window) and works regardless of focus.
`KEY_HINTS_TEXT` is derived from this same table (plus the documented
Enter exception) so the on-screen hints can never drift from what is
actually bound.
"""

from dataclasses import dataclass

_ENTER_HINT = "Enter: enviar"
_HINT_SEPARATOR = " · "


@dataclass(frozen=True)
class KeyBindingSpec:
    """One global key binding: its Tk sequence, the action it triggers, and
    the human-readable key combo shown in the on-screen hints."""

    sequence: str
    action: str
    description: str
    key_display: str


KEY_BINDINGS: tuple[KeyBindingSpec, ...] = (
    KeyBindingSpec("<Control-space>", "on_mic_toggle", "hablar", "Ctrl+Espacio"),
    KeyBindingSpec("<Control-e>", "on_camera_toggle", "cámara", "Ctrl+E"),
    KeyBindingSpec("<Escape>", "on_quit", "salir", "Esc"),
    KeyBindingSpec("<Control-q>", "on_quit", "salir", "Ctrl+Q"),
)


def _build_hints_text() -> str:
    """One hint per unique action, in binding order, plus the Enter exception."""
    seen_actions: set[str] = set()
    hints = []
    for spec in KEY_BINDINGS:
        if spec.action in seen_actions:
            continue
        seen_actions.add(spec.action)
        hints.append(f"{spec.key_display}: {spec.description}")
    hints.insert(len(hints) - 1, _ENTER_HINT)
    return _HINT_SEPARATOR.join(hints)


KEY_HINTS_TEXT = _build_hints_text()
