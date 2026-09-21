"""`app/prompts.txt` must yield one section per model, three sentences each,
and the random pick must be one sentence per model and seed-reproducible."""

import random
import unittest

from app.e2e.prompts import load_prompt_sections, pick_one_per_model

_EXPECTED_MODELS = 10
_SENTENCES_PER_MODEL = 3


class PromptSectionsTests(unittest.TestCase):
    def test_file_has_ten_sections_of_three_sentences(self) -> None:
        sections = load_prompt_sections()
        self.assertEqual(len(sections), _EXPECTED_MODELS)
        for title, sentences in sections.items():
            with self.subTest(section=title):
                self.assertEqual(len(sentences), _SENTENCES_PER_MODEL)

    def test_pick_returns_one_sentence_per_model_from_its_own_section(self) -> None:
        sections = load_prompt_sections()
        picks = pick_one_per_model(sections, random.Random(7))
        self.assertEqual([pick.model_title for pick in picks], list(sections))
        for pick in picks:
            self.assertIn(pick.text, sections[pick.model_title])

    def test_same_seed_picks_the_same_sentences(self) -> None:
        sections = load_prompt_sections()
        first = pick_one_per_model(sections, random.Random(42))
        second = pick_one_per_model(sections, random.Random(42))
        self.assertEqual(first, second)
