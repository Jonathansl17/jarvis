"""`IntentParser` implementation backed by Gemini's structured JSON output."""

import json
from collections.abc import Sequence
from typing import Any

import httpx
from google import genai
from google.genai import errors, types

from app.errors import IntentParsingError
from app.intents.gemini_prompt import build_prompt
from app.intents.models import NeedsInput, ParseResult, ResolvedIntent, Turn

_RESPONSE_MIME_TYPE = "application/json"


class GeminiParser:
    """Parses Spanish text into a model call using Gemini.

    This file is the adapter for `google-genai`: it is the only place in
    `intents/` allowed to construct that library's client.
    """

    def __init__(self, api_key: str, model_name: str, openapi_schema: dict[str, Any]) -> None:
        self._client = genai.Client(api_key=api_key)
        self._model_name = model_name
        self._openapi_schema = openapi_schema

    async def parse(self, text: str, history: Sequence[Turn]) -> ParseResult:
        """Ask Gemini to identify the target model and its fields from `text`."""
        prompt = build_prompt(text, history, self._openapi_schema)
        payload = await self._generate(prompt)
        return _to_parse_result(payload)

    async def _generate(self, prompt: str) -> dict[str, Any]:
        """Call Gemini and parse its response body as JSON."""
        try:
            response = await self._client.aio.models.generate_content(
                model=self._model_name,
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type=_RESPONSE_MIME_TYPE),
            )
        except (errors.APIError, httpx.HTTPError) as exc:
            raise IntentParsingError(f"Gemini request failed: {exc}") from exc
        return _parse_json(response.text)


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
