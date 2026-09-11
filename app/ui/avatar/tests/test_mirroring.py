"""Regression tests for the emotion mirroring policy and its config flag."""

import unittest

from app.emotion.protocol import Emotion
from app.ui.avatar import mirroring


class MirroringPolicyTests(unittest.TestCase):
    def test_hostile_emotions_default_to_mirrored_off(self) -> None:
        """Angry and disgust show on the avatar as themselves by default."""
        self.assertFalse(mirroring.MIRROR_HOSTILE_EMOTIONS)

    def test_angry_and_disgust_pass_through_by_default(self) -> None:
        self.assertIs(mirroring.map_emotion_to_avatar(Emotion.ANGRY), Emotion.ANGRY)
        self.assertIs(mirroring.map_emotion_to_avatar(Emotion.DISGUST), Emotion.DISGUST)

    def test_every_emotion_passes_through_as_itself(self) -> None:
        """Every emotion has its own idle loop now, so none borrows another's
        look — see `emotion_poses.IDLE_LOOP_FOR_EMOTION`."""
        for emotion in Emotion:
            self.assertIs(mirroring.map_emotion_to_avatar(emotion), emotion)


if __name__ == "__main__":
    unittest.main()
