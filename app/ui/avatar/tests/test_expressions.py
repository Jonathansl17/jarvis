"""Regression tests for the per-emotion expression table."""

import unittest

from app.emotion.protocol import Emotion
from app.ui.avatar.expressions import EXPRESSIONS, resolve_expression
from app.ui.avatar.mirroring import map_emotion_to_avatar


class ExpressionTableTests(unittest.TestCase):
    def test_every_emotion_has_an_entry(self) -> None:
        self.assertEqual(set(EXPRESSIONS), set(Emotion))

    def test_every_emotion_overrides_at_least_eyes_or_beak_or_flippers(self) -> None:
        """Neutral is the one legitimate all-default entry; every other
        emotion must override its face to read as a distinct pose."""
        for emotion, expression in EXPRESSIONS.items():
            if emotion is Emotion.NEUTRAL:
                continue
            overrides_something = (
                expression.eyes is not None or expression.beak is not None or expression.flippers is not None
            )
            self.assertTrue(overrides_something, f"{emotion} does not override its face")

    def test_hostile_emotions_are_visually_distinct_from_each_other(self) -> None:
        angry, disgust = EXPRESSIONS[Emotion.ANGRY], EXPRESSIONS[Emotion.DISGUST]
        self.assertNotEqual(angry.eyes, disgust.eyes)
        self.assertNotEqual(angry.flippers, disgust.flippers)
        self.assertNotEqual(angry.cheek_fill, disgust.cheek_fill)

    def test_resolve_expression_applies_the_mirroring_policy(self) -> None:
        for emotion in Emotion:
            self.assertIs(resolve_expression(emotion), EXPRESSIONS[map_emotion_to_avatar(emotion)])

    def test_sad_has_a_desaturated_belly_and_a_tear(self) -> None:
        sad = EXPRESSIONS[Emotion.SAD]
        self.assertNotEqual(sad.belly_fill, EXPRESSIONS[Emotion.NEUTRAL].belly_fill)
        self.assertTrue(sad.extra)

    def test_happy_cheeks_are_larger_and_fully_opaque(self) -> None:
        happy, neutral = EXPRESSIONS[Emotion.HAPPY], EXPRESSIONS[Emotion.NEUTRAL]
        self.assertGreater(happy.cheek_scale, neutral.cheek_scale)
        self.assertGreater(happy.cheek_opacity, neutral.cheek_opacity)


if __name__ == "__main__":
    unittest.main()
