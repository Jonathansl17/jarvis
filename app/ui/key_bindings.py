"""Single source of truth for `JarvisApp`'s key bindings.

`ui/app.py` turns each entry into a Textual `Binding`, and
`ui/widgets/status_bar.py` turns the same entries into the status line's key
hints, so the bindings and their on-screen description never drift apart.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class KeyBindingSpec:
    """One key binding: the key, the action it triggers, and its Spanish hint.

    `key` is Textual's internal key name (see `textual.keys`), which is not
    always what a user would type to reach it — `key_display`, when set,
    overrides it for the status bar hint and Textual's own UI.
    """

    key: str
    action: str
    description: str
    key_display: str | None = None


KEY_BINDINGS: tuple[KeyBindingSpec, ...] = (
    # Textual's internal name for Ctrl+Space is "ctrl+at" (see
    # `textual.keys.KEY_ALIASES`); `key_display` shows the key users actually
    # press. `ctrl+t` is a second binding for the same action, as a fallback
    # for terminals that swallow Ctrl+Space before it reaches the app.
    KeyBindingSpec(
        key="ctrl+at", action="toggle_recording", description="hablar", key_display="ctrl+espacio"
    ),
    KeyBindingSpec(key="ctrl+t", action="toggle_recording", description="hablar"),
    KeyBindingSpec(key="ctrl+e", action="toggle_camera", description="cámara"),
    KeyBindingSpec(key="ctrl+q", action="quit", description="salir"),
)
