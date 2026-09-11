"""Regression tests for `TelecomChurnClassificationExtractor`'s tenure math."""

import unittest

from app.intents.rules.extractors.telecom_churn_classification import (
    TelecomChurnClassificationExtractor,
)


class TelecomChurnClassificationExtractorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.extractor = TelecomChurnClassificationExtractor()

    def test_tenure_in_months_stays_as_is(self) -> None:
        fields = self.extractor.extract("lleva 3 meses de servicio")
        self.assertEqual(fields["tenure"], 3.0)

    def test_tenure_in_years_is_converted_to_months(self) -> None:
        fields = self.extractor.extract("lleva dos años de servicio")
        self.assertEqual(fields["tenure"], 24.0)

    def test_monthly_charge_phrase(self) -> None:
        fields = self.extractor.extract("paga 95 dólares al mes")
        self.assertEqual(fields["MonthlyCharges"], 95.0)
