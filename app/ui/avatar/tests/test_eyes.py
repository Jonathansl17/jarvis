"""Regression test for the eyelid rendering bug: a lid covering only part
of an eye must never leave a visible ring of white sclera around it — sad's
eyes used to render as open white rings ("like earrings") because a
tight-fit lid left gaps at the eye's corners.
"""

import unittest

from app.emotion.protocol import Emotion
from app.ui.avatar.eyes import DISGUST_EYES, FEAR_EYES, LEFT_EYE_BOX, RIGHT_EYE_BOX, SAD_EYES
from app.ui.avatar.expressions import EXPRESSIONS
from app.ui.avatar.reactive_frames import LISTENING_FRAMES
from app.ui.avatar.renderer import render_pose
from app.ui.avatar.shapes import AVATAR_BODY, CANVAS_SIZE_PX

_REST_POSE = LISTENING_FRAMES[0]  # any plain pose; eyes are fully overridden anyway
_HEAD_RGB = (int(AVATAR_BODY[1:3], 16), int(AVATAR_BODY[3:5], 16), int(AVATAR_BODY[5:7], 16))


def _top_center(box: tuple[int, int, int, int]) -> tuple[int, int]:
    x0, y0, x1, _ = box
    return (x0 + x1) // 2, y0 + 1


class EyelidNoRingTests(unittest.TestCase):
    def test_sad_lids_cover_the_top_of_both_eyes_with_no_gap(self) -> None:
        self._assert_lid_covers(Emotion.SAD, LEFT_EYE_BOX)
        self._assert_lid_covers(Emotion.SAD, RIGHT_EYE_BOX)

    def test_fear_worried_lids_cover_the_top_of_both_eyes_with_no_gap(self) -> None:
        self._assert_lid_covers(Emotion.FEAR, LEFT_EYE_BOX)
        self._assert_lid_covers(Emotion.FEAR, RIGHT_EYE_BOX)

    def test_disgust_squinted_eye_lid_covers_with_no_gap(self) -> None:
        self._assert_lid_covers(Emotion.DISGUST, RIGHT_EYE_BOX)

    def _assert_lid_covers(self, emotion, box: tuple[int, int, int, int]) -> None:
        image = render_pose(_REST_POSE, EXPRESSIONS[emotion], (CANVAS_SIZE_PX, CANVAS_SIZE_PX))
        pixel = image.getpixel(_top_center(box))[:3]
        self.assertEqual(pixel, _HEAD_RGB, f"{emotion} left a gap at the top of its eye lid")

    def test_every_redesigned_eye_table_is_non_empty(self) -> None:
        for eyes in (SAD_EYES, FEAR_EYES, DISGUST_EYES):
            self.assertTrue(eyes)


if __name__ == "__main__":
    unittest.main()
