"""Regression tests for `dates.py`'s calendar-phrase parsing."""

import unittest
from datetime import date
from unittest import mock

from app.intents.rules.dates import find_day_of_month, find_full_date
from app.intents.rules.tables.calendar import MONTH_NAMES


class FindDayOfMonthTests(unittest.TestCase):
    def test_reads_the_day_before_the_month_name(self) -> None:
        self.assertEqual(find_day_of_month("el viernes 19 de diciembre a las 6", MONTH_NAMES), 19)

    def test_no_date_phrase_is_none(self) -> None:
        self.assertIsNone(find_day_of_month("el viernes a las 6", MONTH_NAMES))


class FindFullDateTests(unittest.TestCase):
    def test_reads_a_full_day_month_year_phrase(self) -> None:
        text = "el 10 de septiembre de 2017 con un volumen total"
        self.assertEqual(find_full_date(text, MONTH_NAMES), "2017-09-10")

    def test_hoy_resolves_to_todays_date(self) -> None:
        with mock.patch("app.intents.rules.dates.date") as mock_date:
            mock_date.today.return_value = date(2026, 1, 1)
            self.assertEqual(find_full_date("el aguacate hoy", MONTH_NAMES), "2026-01-01")

    def test_no_date_phrase_is_none(self) -> None:
        self.assertIsNone(find_full_date("el aguacate orgánico", MONTH_NAMES))
