"""`IntentParser` implementation backed by Gemini's structured JSON output."""

import json
from collections.abc import Sequence
from typing import Any

import httpx
from google import genai
from google.genai import errors, types

from app.errors import IntentParsingError
from app.intents.gemini_prompt import build_system_instruction, build_user_content
from app.intents.models import NeedsInput, ParseResult, ResolvedIntent, Turn

_RESPONSE_MIME_TYPE = "application/json"
# A model this old (quota exhausted) or this missing (retired) is skipped in
# favor of the next one in the chain, rather than failing the whole parse.
_RETRYABLE_STATUS_CODES = (429, 404)
_FALLBACK_NOTICE_TEMPLATE = "Gemini: '{failed_model}' no disponible, usando '{next_model}'."


class GeminiParser:
    """Parses Spanish text into a model call using Gemini.

    Tries each model in `model_names`, in order, moving to the next one on a
    quota-exhausted (429) or retired-model (404) error, so a free-tier daily
    limit on the first model does not take Gemini out of the conversation.
    Once a model in the chain fails, later calls skip straight past it
    instead of re-trying and re-logging every turn.

    This file is the adapter for `google-genai`: it is the only place in
    `intents/` allowed to construct that library's client.
    """

    def __init__(self, api_key: str, model_names: Sequence[str], openapi_schema: dict[str, Any]) -> None:
        if not model_names:
            raise ValueError("GeminiParser needs at least one model name")
        self._client = genai.Client(api_key=api_key)
        self._model_names = tuple(model_names)
        self._active_index = 0
        self._pending_notice: str | None = None
        self._system_instruction = build_system_instruction(openapi_schema)

    async def parse(self, text: str, history: Sequence[Turn]) -> ParseResult:
        """Ask Gemini to identify the target model and its fields from `text`."""
        content = build_user_content(text, history)
        payload = await self._generate(content)
        return _to_parse_result(payload)

    def take_fallback_notice(self) -> str | None:
        """Return and clear the notice for the most recent model fallback, if any."""
        notice, self._pending_notice = self._pending_notice, None
        return notice

    async def _generate(self, content: str) -> dict[str, Any]:
        """Call Gemini, advancing through `_model_names` on a retryable error."""
        while True:
            model_name = self._model_names[self._active_index]
            try:
                response = await self._client.aio.models.generate_content(
                    model=model_name,
                    contents=content,
                    config=types.GenerateContentConfig(
                        response_mime_type=_RESPONSE_MIME_TYPE,
                        system_instruction=self._system_instruction,
                    ),
                )
            except errors.APIError as exc:
                self._advance_past(model_name, exc)
                continue
            except httpx.HTTPError as exc:
                raise IntentParsingError(f"Gemini request failed: {exc}") from exc
            return _parse_json(response.text)

    def _advance_past(self, failed_model: str, exc: errors.APIError) -> None:
        """Move to the next model in the chain, or raise if none are left."""
        if exc.code not in _RETRYABLE_STATUS_CODES or self._active_index + 1 >= len(self._model_names):
            raise IntentParsingError(f"Gemini request failed: {exc}") from exc
        self._active_index += 1
        next_model = self._model_names[self._active_index]
        self._pending_notice = _FALLBACK_NOTICE_TEMPLATE.format(failed_model=failed_model, next_model=next_model)


def _parse_json(raw: str | None) -> dict[str, Any]:
    """Decode Gemini's response text as a JSON object."""
    if not raw:
        raise IntentParsingError("Gemini returned an empty response")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise IntentParsingError(f"Gemini returned invalid JSON: {raw!r}") from exc


def _to_parse_result(payload: dict[str, Any]) -> ParseResult:
    """Turn Gemini's JSON payload into a `ParseResult`."""
    try:
        model_name = payload["model_name"]
        fields = payload["fields"]
        missing = payload.get("missing", [])
    except KeyError as exc:
        raise IntentParsingError(f"Gemini response missing key: {exc}") from exc
    if not model_name:
        raise IntentParsingError("Gemini could not match the request to any model")
    if missing:
        return NeedsInput(model_name=model_name, fields=fields, missing=missing)
    return ResolvedIntent(model_name=model_name, fields=fields)
