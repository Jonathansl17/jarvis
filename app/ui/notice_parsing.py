"""Extracts a short IA-field label from a dialogue-layer fallback notice.

`DialogueOrchestrator`'s `system_notice` is a full Spanish sentence meant
for a chat line (e.g. `"Gemini: 'x' no disponible, usando 'y'."`); the
status strip's IA field instead needs just the model name it switched to.
Parsing it here — rather than changing `dialogue/gemini_parser.py`'s
contract — keeps this UI-only concern out of the dialogue layer.
"""

import re

_FALLBACK_MODEL_PATTERN = re.compile(r"usando '([^']+)'")


def extract_fallback_model(notice: str) -> str | None:
    """Return the model name a Gemini fallback notice switched to, if any."""
    match = _FALLBACK_MODEL_PATTERN.search(notice)
    return match.group(1) if match else None
