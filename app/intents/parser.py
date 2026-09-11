"""The contract every intent source (rules, Gemini, composite) satisfies."""

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from app.intents.models import ParseResult, Turn


class IntentParser(Protocol):
    """Turns free text plus conversation history into a parse result."""

    async def parse(self, text: str, history: Sequence[Turn]) -> ParseResult: ...


@runtime_checkable
class FallbackNoticeSource(Protocol):
    """An `IntentParser` that can report a one-off notice about a fallback.

    Optional: most parsers (e.g. `RulesParser`) never fall back to anything
    and so never implement this.
    """

    def take_fallback_notice(self) -> str | None: ...
