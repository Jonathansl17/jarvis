"""Regression tests for `CarPriceRegressionExtractor`."""

import unittest

from app.intents.rules.extractors.car_price_regression import CarPriceRegressionExtractor


class CarPriceRegressionExtractorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.extractor = CarPriceRegressionExtractor()

    def test_first_owner_phrase_resolves_to_zero(self) -> None:
        fields = self.extractor.extract("un carro con un solo dueño")
        self.assertEqual(fields["owner"], 0)

    def test_second_owner_phrase_resolves_to_one(self) -> None:
        fields = self.extractor.extract("un carro con segundo dueño")
        self.assertEqual(fields["owner"], 1)

    def test_owner_defaults_to_zero_when_unmentioned(self) -> None:
        fields = self.extractor.extract("un carro diesel del 2015")
        self.assertEqual(fields["owner"], 0)

    def test_price_is_not_confused_with_the_surrounding_question(self) -> None:
        text = "cuánto vale un carro diesel del 2015 que nuevo costó 10 lakhs"
        fields = self.extractor.extract(text)
        self.assertEqual(fields["present_price"], 10.0)
