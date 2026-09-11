"""Keyword-based `IntentParser` implementation with no network I/O."""

from collections.abc import Sequence

from app.errors import IntentParsingError
from app.intents.models import NeedsInput, ParseResult, ResolvedIntent, Turn
from app.intents.rules.registry import FIELD_EXTRACTORS, MODEL_KEYWORDS


class RulesParser:
    """Matches Spanish text to a model by keyword, then extracts its fields."""

    async def parse(self, text: str, history: Sequence[Turn]) -> ParseResult:
        """Identify the target model from `text` and extract its fields.

        `history` is accepted to satisfy `IntentParser`; this parser is
        stateless and only ever looks at the current utterance.
        """
        model_name = self._match_model(text)
        extractor = FIELD_EXTRACTORS[model_name]
        fields = extractor.extract(text)
        missing = [name for name in extractor.required_fields if name not in fields]
        if missing:
            return NeedsInput(model_name=model_name, fields=fields, missing=missing)
        return ResolvedIntent(model_name=model_name, fields=fields)

    @staticmethod
    def _match_model(text: str) -> str:
        """Return the first model whose trigger keyword appears in `text`."""
        lowered = text.lower()
        for model_name, keywords in MODEL_KEYWORDS.items():
            if any(keyword in lowered for keyword in keywords):
                return model_name
        raise IntentParsingError(f"no known model matched in: {text!r}")
