"""Regression tests for `quantities.py`'s zero-cue and adjacency helpers."""

import unittest

from app.intents.rules.quantities import find_number_immediately_before, find_quantity_near


class FindQuantityNearTests(unittest.TestCase):
    def test_returns_the_nearby_number_when_present(self) -> None:
        self.assertEqual(find_quantity_near("7 mil bolsas pequeñas", ("bolsas pequeñas",)), 7000.0)

    def test_none_cue_reads_as_zero(self) -> None:
        self.assertEqual(find_quantity_near("ninguna extragrande", ("extragrande",)), 0.0)

    def test_missing_field_is_none(self) -> None:
        self.assertIsNone(find_quantity_near("sin datos relevantes", ("extragrande",)))


class FindNumberImmediatelyBeforeTests(unittest.TestCase):
    def test_adjacent_clauses_do_not_bleed_into_each_other(self) -> None:
        text = "30 de dióxido de azufre libre, 120 de dióxido de azufre total"
        self.assertEqual(find_number_immediately_before(text, ("dióxido de azufre libre",)), 30.0)
        self.assertEqual(find_number_immediately_before(text, ("dióxido de azufre total",)), 120.0)

    def test_does_not_anchor_to_a_code_number_in_the_phrase(self) -> None:
        text = "5 mil del código 4046, 6 mil del 4225"
        self.assertEqual(find_number_immediately_before(text, ("del código 4046", "del 4046")), 5_000.0)
        self.assertEqual(find_number_immediately_before(text, ("del código 4225", "del 4225")), 6_000.0)

    def test_bare_multiplier_word_before_the_phrase(self) -> None:
        self.assertEqual(find_number_immediately_before("mil del 4770", ("del 4770",)), 1_000.0)

    def test_no_number_before_the_phrase_is_none(self) -> None:
        self.assertIsNone(find_number_immediately_before("nada del 4770", ("del 4770",)))
