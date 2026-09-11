"""Regression tests for `FlightDelayRegressionExtractor`."""

import unittest

from app.intents.rules.extractors.flight_delay_regression import FlightDelayRegressionExtractor

_SENTENCE = (
    "el vuelo de American Airlines de Chicago a Los Ángeles el viernes "
    "19 de diciembre a las 6 de la tarde, con 1745 millas de distancia"
)


class FlightDelayRegressionExtractorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fields = FlightDelayRegressionExtractor().extract(_SENTENCE)

    def test_carrier_name_resolves_to_its_iata_code(self) -> None:
        self.assertEqual(self.fields["carrier"], "AA")

    def test_route_cities_resolve_in_reading_order(self) -> None:
        self.assertEqual(self.fields["origin"], "ORD")
        self.assertEqual(self.fields["dest"], "LAX")

    def test_day_of_month_reads_the_day_before_the_month_name(self) -> None:
        self.assertEqual(self.fields["day_of_month"], 19)

    def test_afternoon_hour_is_converted_to_24_hour_clock(self) -> None:
        self.assertEqual(self.fields["dep_hour"], 18)

    def test_morning_hour_is_left_unchanged(self) -> None:
        fields = FlightDelayRegressionExtractor().extract("el vuelo sale a las 9 de la mañana")
        self.assertEqual(fields["dep_hour"], 9)
