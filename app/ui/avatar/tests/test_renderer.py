"""Regression tests for `render_pose`'s z-order: the belly and cheeks must
never cover the beak, tongue, or other face decorations drawn on top of
them (a prior bug hid the lower half of the open-mouth speaking beak).
"""

import unittest

from app.emotion.protocol import Emotion
from app.ui.avatar.expressions import EXPRESSIONS, resolve_expression
from app.ui.avatar.reactive_frames import SPEAKING_FRAMES
from app.ui.avatar.renderer import render_pose
from app.ui.avatar.shapes import AVATAR_BEAK_ANGRY, AVATAR_BEAK_FOOT, CANVAS_SIZE_PX

# The mouth area around the speaking frames' beak, in the untouched 260x260
# canvas — wide enough to cover the small vertical bounce the open-mouth
# frame applies, without depending on its exact offset.
_MOUTH_BOX = (110, 95, 150, 125)
_BEAK_OPEN_FRAME_INDEX = 2


class SpeakingBeakZOrderTests(unittest.TestCase):
    def test_open_beak_is_not_covered_by_the_belly_under_neutral(self) -> None:
        self._assert_beak_color_visible(emotion=None, beak_color=AVATAR_BEAK_FOOT)

    def test_open_beak_is_not_covered_by_the_belly_under_surprise(self) -> None:
        self._assert_beak_color_visible(emotion=Emotion.SURPRISE, beak_color=AVATAR_BEAK_FOOT)

    def test_happy_smile_beak_is_not_covered_by_the_belly(self) -> None:
        self._assert_beak_color_visible(emotion=Emotion.HAPPY, beak_color=AVATAR_BEAK_FOOT)

    def test_angry_flat_beak_is_not_covered_by_the_belly(self) -> None:
        """Angry's own pose (bypassing the neutral mirroring policy — see
        `test_mirroring.py`), the way the sheet script renders it."""
        pose = SPEAKING_FRAMES[_BEAK_OPEN_FRAME_INDEX]
        image = render_pose(pose, EXPRESSIONS[Emotion.ANGRY], (CANVAS_SIZE_PX, CANVAS_SIZE_PX))
        self.assertTrue(_color_present_in_box(image, _MOUTH_BOX, _hex_to_rgb(AVATAR_BEAK_ANGRY)))

    def _assert_beak_color_visible(self, emotion: Emotion | None, beak_color: str) -> None:
        image = self._render(emotion)
        self.assertTrue(
            _color_present_in_box(image, _MOUTH_BOX, _hex_to_rgb(beak_color)),
            f"{beak_color} not found in the mouth area for emotion={emotion}",
        )

    def _render(self, emotion: Emotion | None):
        pose = SPEAKING_FRAMES[_BEAK_OPEN_FRAME_INDEX]
        expression = resolve_expression(emotion) if emotion is not None else None
        return render_pose(pose, expression, (CANVAS_SIZE_PX, CANVAS_SIZE_PX))


def _color_present_in_box(image, box: tuple[int, int, int, int], rgb: tuple[int, int, int]) -> bool:
    x0, y0, x1, y1 = box
    region = image.crop(box)
    return any(region.getpixel((x, y))[:3] == rgb for x in range(x1 - x0) for y in range(y1 - y0))


def _hex_to_rgb(color: str) -> tuple[int, int, int]:
    return (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))


if __name__ == "__main__":
    unittest.main()
