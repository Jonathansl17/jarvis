"""Composes two `IntentParser`s: Gemini first, rules as the fallback."""

from collections.abc import Sequence

from app.errors import IntentParsingError
from app.intents.models import ParseResult, Turn
from app.intents.parser import IntentParser


class CompositeIntentParser:
    """Tries `primary`, falling back to `fallback` on any parsing failure.

    Neither parser knows about the other's existence — this class is the
    only place the fallback behaviour is decided.
    """

    def __init__(self, primary: IntentParser, fallback: IntentParser) -> None:
        self._primary = primary
        self._fallback = fallback

    async def parse(self, text: str, history: Sequence[Turn]) -> ParseResult:
        """Parse with `primary`; on `IntentParsingError`, retry with `fallback`."""
        try:
            return await self._primary.parse(text, history)
        except IntentParsingError:
            return await self._fallback.parse(text, history)
