"""Regression tests for `AvocadoPriceRegressionExtractor`."""

import unittest

from app.intents.rules.extractors.avocado_price_regression import AvocadoPriceRegressionExtractor

_SENTENCE = (
    "el aguacate orgánico en San Francisco el 10 de septiembre de 2017 con un "
    "volumen total de 20 mil, 5 mil del código 4046, 6 mil del 4225, mil del "
    "4770, 8 mil bolsas en total, 7 mil bolsas pequeñas, mil grandes y "
    "ninguna extragrande"
)


class AvocadoPriceRegressionExtractorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fields = AvocadoPriceRegressionExtractor().extract(_SENTENCE)

    def test_region_name_resolves_to_the_dataset_string(self) -> None:
        self.assertEqual(self.fields["region"], "SanFrancisco")

    def test_full_date_phrase_resolves_to_iso(self) -> None:
        self.assertEqual(self.fields["date"], "2017-09-10")

    def test_total_volume_is_not_confused_with_the_leading_article(self) -> None:
        self.assertEqual(self.fields["total_volume"], 20_000.0)

    def test_plu_quantities_are_not_confused_with_their_own_codes(self) -> None:
        self.assertEqual(self.fields["plu_4046"], 5_000.0)
        self.assertEqual(self.fields["plu_4225"], 6_000.0)
        self.assertEqual(self.fields["plu_4770"], 1_000.0)

    def test_bag_counts(self) -> None:
        self.assertEqual(self.fields["total_bags"], 8_000.0)
        self.assertEqual(self.fields["small_bags"], 7_000.0)
        self.assertEqual(self.fields["large_bags"], 1_000.0)

    def test_none_extra_large_bags_reads_as_zero(self) -> None:
        self.assertEqual(self.fields["xlarge_bags"], 0.0)
