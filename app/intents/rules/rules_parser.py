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
        """Return the model whose trigger keywords match `text` best.

        The score is the length of the longest matched keyword, then the number
        of matches, so a specific phrase outweighs a generic word shared with
        another model.
        """
        lowered = text.lower()
        scores = {
            model_name: (
                max((len(keyword) for keyword in keywords if keyword in lowered), default=0),
                sum(keyword in lowered for keyword in keywords),
            )
            for model_name, keywords in MODEL_KEYWORDS.items()
        }
        best_model, best_score = max(scores.items(), key=lambda item: item[1])
        if best_score[0] == 0:
            raise IntentParsingError(f"no known model matched in: {text!r}")
        return best_model
