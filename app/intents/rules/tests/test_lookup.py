"""Regression tests for `lookup.py`'s table-driven name matching."""

import unittest

from app.intents.rules.lookup import find_ordered_values, find_value_by_longest_key


class FindValueByLongestKeyTests(unittest.TestCase):
    _TABLE = {"American": "AA", "American Eagle": "MQ"}

    def test_prefers_the_longest_matching_name(self) -> None:
        self.assertEqual(find_value_by_longest_key("vuelo de American Eagle", self._TABLE), "MQ")

    def test_falls_back_to_the_only_match(self) -> None:
        self.assertEqual(find_value_by_longest_key("vuelo de American Airlines", self._TABLE), "AA")

    def test_no_match_is_none(self) -> None:
        self.assertIsNone(find_value_by_longest_key("vuelo de Delta", self._TABLE))


class FindOrderedValuesTests(unittest.TestCase):
    _AIRPORTS = {"Chicago": "ORD", "Los Ángeles": "LAX"}

    def test_returns_values_in_reading_order(self) -> None:
        result = find_ordered_values("vuelo de Chicago a Los Ángeles", self._AIRPORTS)
        self.assertEqual(result, ["ORD", "LAX"])

    def test_reversed_mention_order_is_preserved(self) -> None:
        result = find_ordered_values("vuelo de Los Ángeles a Chicago", self._AIRPORTS)
        self.assertEqual(result, ["LAX", "ORD"])

    def test_single_match_returns_one_value(self) -> None:
        self.assertEqual(find_ordered_values("vuelo desde Chicago", self._AIRPORTS), ["ORD"])
