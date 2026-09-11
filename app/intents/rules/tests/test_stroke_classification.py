"""Regression tests for `StrokeClassificationExtractor`'s boolean cues."""

import unittest

from app.intents.rules.extractors.stroke_classification import StrokeClassificationExtractor


class StrokeClassificationExtractorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.extractor = StrokeClassificationExtractor()

    def test_hipertenso_adjective_is_true(self) -> None:
        fields = self.extractor.extract("un hombre hipertenso")
        self.assertTrue(fields["hypertension"])

    def test_sin_hipertension_is_false(self) -> None:
        fields = self.extractor.extract("un hombre sin hipertensión")
        self.assertFalse(fields["hypertension"])

    def test_sin_enfermedad_del_corazon_is_false(self) -> None:
        fields = self.extractor.extract("un hombre sin enfermedad del corazón")
        self.assertFalse(fields["heart_disease"])

    def test_con_enfermedad_del_corazon_is_true(self) -> None:
        fields = self.extractor.extract("un hombre con enfermedad del corazón")
        self.assertTrue(fields["heart_disease"])
