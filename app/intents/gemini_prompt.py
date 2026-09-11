"""Builds the system instruction and per-turn content sent to Gemini."""

import json
from collections.abc import Sequence
from typing import Any

from app.intents.gemini_model_catalog import build_model_catalog_text
from app.intents.models import Turn

_SYSTEM_INSTRUCTION_TEMPLATE = """\
You are the intent parser for JarvisTEC, a Spanish-speaking voice assistant \
that calls one of ten machine learning models. Given the user's latest \
message and the conversation so far, respond with a single JSON object and \
nothing else, shaped exactly as:

{{"model_name": "<one of the model names below>",
  "fields": {{"<field name>": "<value>"}},
  "missing": ["<names of required fields you could not confidently infer>"]}}

The ten models, each with a one-line description, common Spanish synonyms
for what triggers it, and its own field-inference rules:
{model_catalog}

Field values must follow the JSON schema below, one entry per model
(required fields, types, and enums). Only include a field in "missing" when
it is required by its model's schema, cannot be inferred from the
conversation, and has no sensible default (a per-model rule above may give
one, e.g. car_price_regression's "owner"). Never ask for an optional field,
and never ask for a field a casual user would expect the assistant to work
out, except one it truly has no basis for (e.g. Contract or InternetService
on a first mention, which have no safe default).

General inference rules, on top of each model's own above:
- "mañana" means 1 day ahead, "pasado mañana" 2, "una semana" 7, "un mes" 30
  (or the field's schema maximum if that is lower).
- "este año" means the current year.
- Numbers may be spelled out in Spanish ("cuarenta mil" = 40000, "mil
  quinientos" = 1500) or abbreviated ("40 mil" = 40000).

The message was transcribed by speech-to-text and may contain mishearings
(e.g. "dientes" for "días", "Yalvis" or "Yarvis" for "JarvisTEC"); use
context to recover the intended word rather than taking it literally.

Only include fields you can confidently read or infer from the
conversation. Do not invent values with no basis in the message. If no
model matches the request, set "model_name" to null and "fields" to an
empty object.

JSON schema:
{schema}
"""

_USER_CONTENT_TEMPLATE = """\
Conversation so far:
{history}

User's latest message:
{text}
"""

_NO_HISTORY_PLACEHOLDER = "(no previous turns)"


def build_system_instruction(openapi_schema: dict[str, Any]) -> str:
    """Render the fixed system instruction Gemini receives for every call."""
    return _SYSTEM_INSTRUCTION_TEMPLATE.format(
        model_catalog=build_model_catalog_text(),
        schema=json.dumps(openapi_schema, ensure_ascii=False),
    )


def build_user_content(text: str, history: Sequence[Turn]) -> str:
    """Render the per-call content: prior turns plus the latest message."""
    return _USER_CONTENT_TEMPLATE.format(history=_render_history(history), text=text)


def _render_history(history: Sequence[Turn]) -> str:
    """Render prior turns as `speaker: text` lines, oldest first."""
    if not history:
        return _NO_HISTORY_PLACEHOLDER
    return "\n".join(f"{turn.speaker}: {turn.text}" for turn in history)
