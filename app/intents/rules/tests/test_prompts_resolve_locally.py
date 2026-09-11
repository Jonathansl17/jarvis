"""End-to-end regression test: every `app/prompts.txt` example sentence must
resolve through the local rules parser alone, with no missing fields, so the
app keeps working with Gemini unavailable.
"""

import unittest
from pathlib import Path

from app.intents.models import ResolvedIntent
from app.intents.rules.rules_parser import RulesParser
from app.intents.wake_word import strip_wake_word

_PROMPTS_PATH = Path(__file__).resolve().parents[3] / "prompts.txt"
_PROMPT_PREFIX = "JarvisTEC"


def _load_example_sentences() -> list[str]:
    lines = _PROMPTS_PATH.read_text(encoding="utf-8").splitlines()
    return [line for line in lines if line.startswith(_PROMPT_PREFIX)]


class PromptsResolveLocallyTests(unittest.IsolatedAsyncioTestCase):
    async def test_every_example_sentence_resolves_with_no_missing_fields(self) -> None:
        parser = RulesParser()
        sentences = _load_example_sentences()
        self.assertEqual(len(sentences), 10, "expected all ten example sentences")
        for sentence in sentences:
            text = strip_wake_word(sentence)
            with self.subTest(sentence=sentence):
                result = await parser.parse(text, [])
                self.assertIsInstance(result, ResolvedIntent, f"missing fields: {getattr(result, 'missing', None)}")
