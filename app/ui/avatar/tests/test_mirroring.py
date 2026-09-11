"""Regression tests for the emotion mirroring policy and its config flag."""

import unittest

from app.emotion.protocol import Emotion
from app.ui.avatar import mirroring


class MirroringPolicyTests(unittest.TestCase):
    def test_hostile_emotions_default_to_mirrored_on(self) -> None:
        self.assertTrue(mirroring.MIRROR_HOSTILE_EMOTIONS)

    def test_angry_and_disgust_mirror_to_neutral_by_default(self) -> None:
        self.assertIs(mirroring.map_emotion_to_avatar(Emotion.ANGRY), Emotion.NEUTRAL)
        self.assertIs(mirroring.map_emotion_to_avatar(Emotion.DISGUST), Emotion.NEUTRAL)

    def test_non_hostile_emotions_pass_through_or_map_to_surprise(self) -> None:
        self.assertIs(mirroring.map_emotion_to_avatar(Emotion.HAPPY), Emotion.HAPPY)
        self.assertIs(mirroring.map_emotion_to_avatar(Emotion.SAD), Emotion.SAD)
        self.assertIs(mirroring.map_emotion_to_avatar(Emotion.FEAR), Emotion.SURPRISE)


if __name__ == "__main__":
    unittest.main()
