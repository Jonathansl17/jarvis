"""Regression tests for `number_words.py`'s spelled-out number parsing."""

import unittest

from app.intents.rules.number_words import find_number_words


class FindNumberWordsTests(unittest.TestCase):
    def test_bare_indefinite_article_is_not_a_number(self) -> None:
        """"un"/"una" alone are almost always articles, not the number one."""
        self.assertEqual(find_number_words("un carro usado"), [])
        self.assertEqual(find_number_words("una agencia"), [])

    def test_combined_number_words_still_parse(self) -> None:
        matches = find_number_words("cuarenta mil doscientos")
        self.assertEqual([match.value for match in matches], [40_200.0])

    def test_bare_multiplier_word_means_its_own_value(self) -> None:
        matches = find_number_words("mil grandes")
        self.assertEqual([match.value for match in matches], [1_000.0])
