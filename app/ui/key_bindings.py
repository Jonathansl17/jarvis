"""Single source of truth for `JarvisApp`'s key bindings.

`ui/app.py` turns each entry into a Textual `Binding`, and
`ui/widgets/status_bar.py` turns the same entries into the status line's key
hints, so the bindings and their on-screen description never drift apart.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class KeyBindingSpec:
    """One key binding: the key, the action it triggers, and its Spanish hint."""

    key: str
    action: str
    description: str


KEY_BINDINGS: tuple[KeyBindingSpec, ...] = (
    KeyBindingSpec(key="space", action="toggle_recording", description="hablar"),
    KeyBindingSpec(key="ctrl+e", action="toggle_camera", description="cámara"),
    KeyBindingSpec(key="ctrl+q", action="quit", description="salir"),
)
