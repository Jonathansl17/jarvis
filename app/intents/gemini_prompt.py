"""Builds the prompt sent to Gemini to parse one user utterance."""

import json
from collections.abc import Sequence
from typing import Any

from app.intents.models import Turn

_INSTRUCTIONS = """\
You are the intent parser for a Spanish-speaking voice assistant that calls
one of the machine learning models described in the OpenAPI schema below.
Given the user's latest message and the conversation so far, respond with a
single JSON object and nothing else, shaped exactly as:

{{"model_name": "<one of the model names in the schema>",
  "fields": {{"<field name>": "<value>"}},
  "missing": ["<names of required fields you could not find in the message>"]}}

Only include fields you can confidently read from the conversation. Do not
invent values. If no model in the schema matches the request, set
"model_name" to null and "fields" to an empty object.

OpenAPI schema:
{schema}

Conversation so far:
{history}

User's latest message:
{text}
"""

_NO_HISTORY_PLACEHOLDER = "(no previous turns)"


def build_prompt(text: str, history: Sequence[Turn], openapi_schema: dict[str, Any]) -> str:
    """Render the full prompt Gemini receives for one parse call."""
    return _INSTRUCTIONS.format(
        schema=json.dumps(openapi_schema, ensure_ascii=False),
        history=_render_history(history),
        text=text,
    )


def _render_history(history: Sequence[Turn]) -> str:
    """Render prior turns as `speaker: text` lines, oldest first."""
    if not history:
        return _NO_HISTORY_PLACEHOLDER
    return "\n".join(f"{turn.speaker}: {turn.text}" for turn in history)
