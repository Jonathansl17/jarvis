"""Renders the turn-by-turn transcript (§5 of the design spec)."""

from datetime import datetime

from textual.widgets import RichLog

_TIMESTAMP_FORMAT = "%H:%M:%S"
_LINE_TEMPLATE = "[{color}]{timestamp}  {label}[/{color}]  {text}"

_USER_LABEL = "TÚ"
_ASSISTANT_LABEL = "JTC"
_SYSTEM_LABEL = "SYS"

_USER_COLOR = "#59C7F2"
_ASSISTANT_COLOR = "#59F2C4"
_SYSTEM_COLOR = "#8A9385"

_SPEAKER_STYLE: dict[str, tuple[str, str]] = {
    "user": (_USER_LABEL, _USER_COLOR),
    "assistant": (_ASSISTANT_LABEL, _ASSISTANT_COLOR),
    "system": (_SYSTEM_LABEL, _SYSTEM_COLOR),
}


class ConversationLog(RichLog):
    """Appends one labeled, timestamped line per turn, auto-scrolling down."""

    def __init__(self, **kwargs: object) -> None:
        # `min_width` must stay below the panel's usual content width or it
        # would override `shrink` and force horizontal scrolling instead of
        # the word-wrap the design spec requires for long lines (§4).
        super().__init__(markup=True, wrap=True, min_width=1, auto_scroll=True, **kwargs)

    def append_turn(self, speaker: str, text: str) -> None:
        """Append one line for `speaker` ("user", "assistant", or "system")."""
        label, color = _SPEAKER_STYLE[speaker]
        timestamp = datetime.now().strftime(_TIMESTAMP_FORMAT)
        self.write(_LINE_TEMPLATE.format(color=color, timestamp=timestamp, label=label, text=text))
