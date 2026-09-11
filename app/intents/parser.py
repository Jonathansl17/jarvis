"""The contract every intent source (rules, Gemini, composite) satisfies."""

from collections.abc import Sequence
from typing import Protocol

from app.intents.models import ParseResult, Turn


class IntentParser(Protocol):
    """Turns free text plus conversation history into a parse result."""

    async def parse(self, text: str, history: Sequence[Turn]) -> ParseResult: ...
