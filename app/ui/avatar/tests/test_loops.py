"""Regression tests for the per-emotion idle loops: every emotion has its
own loop of at least 8 frames, the reaction transition is 3 frames, and
every frame renders without error at the app's own 380x380 avatar size.
"""

import unittest

from app.emotion.protocol import Emotion
from app.ui.avatar.emotion_poses import IDLE_LOOP_FOR_EMOTION
from app.ui.avatar.expressions import resolve_expression
from app.ui.avatar.idle_frames import IDLE_FRAMES, IDLE_TRANSITION_FRAME_COUNT
from app.ui.avatar.loops import (
    ANGRY_FRAMES,
    DISGUST_FRAMES,
    FEAR_FRAMES,
    HAPPY_FRAMES,
    SAD_FRAMES,
    SURPRISE_FRAMES,
)
from app.ui.avatar.decorations import EXCLAMATION_MARK
from app.ui.avatar.renderer import render_pose

_MIN_LOOP_FRAME_COUNT = 8
_AVATAR_SIZE_PX = (380, 380)
_REST_FRAME_INDEX = 0

_LOOP_BY_EMOTION = {
    Emotion.HAPPY: HAPPY_FRAMES,
    Emotion.SAD: SAD_FRAMES,
    Emotion.ANGRY: ANGRY_FRAMES,
    Emotion.SURPRISE: SURPRISE_FRAMES,
    Emotion.FEAR: FEAR_FRAMES,
    Emotion.DISGUST: DISGUST_FRAMES,
}


class LoopFrameCountTests(unittest.TestCase):
    def test_every_emotion_has_its_own_loop_of_at_least_eight_frames(self) -> None:
        for emotion, frames in _LOOP_BY_EMOTION.items():
            self.assertGreaterEqual(len(frames), _MIN_LOOP_FRAME_COUNT, f"{emotion} has too few frames")

    def test_neutral_has_no_own_loop(self) -> None:
        self.assertNotIn(Emotion.NEUTRAL, IDLE_LOOP_FOR_EMOTION)

    def test_every_emotion_but_neutral_is_registered_in_idle_loop_for_emotion(self) -> None:
        for emotion in _LOOP_BY_EMOTION:
            self.assertIn(emotion, IDLE_LOOP_FOR_EMOTION)
            self.assertEqual(IDLE_LOOP_FOR_EMOTION[emotion].frame_count, len(_LOOP_BY_EMOTION[emotion]))

    def test_transition_is_three_frames(self) -> None:
        self.assertEqual(IDLE_TRANSITION_FRAME_COUNT, 3)


class LoopRenderTests(unittest.TestCase):
    def test_every_emotion_loop_frame_renders_at_the_avatar_size(self) -> None:
        for emotion, frames in _LOOP_BY_EMOTION.items():
            expression = resolve_expression(emotion)
            for index, pose in enumerate(frames):
                with self.subTest(emotion=emotion, frame=index):
                    image = render_pose(pose, expression, _AVATAR_SIZE_PX)
                    self.assertEqual(image.size, _AVATAR_SIZE_PX)

    def test_every_idle_frame_renders_without_a_resolved_expression(self) -> None:
        """Neutral (and any state with no emotion set) uses `expression=None`."""
        for index, pose in enumerate(IDLE_FRAMES):
            with self.subTest(frame=index):
                image = render_pose(pose, None, _AVATAR_SIZE_PX)
                self.assertEqual(image.size, _AVATAR_SIZE_PX)


class LoopDistinctionTests(unittest.TestCase):
    def test_every_emotions_rest_frame_renders_differently_from_every_other(self) -> None:
        """Each emotion's own loop must actually look distinct — a wrong
        lookup silently showing another emotion's frames would still pass a
        "renders fine" check but fail this one."""
        images_by_emotion = {
            emotion: render_pose(frames[_REST_FRAME_INDEX], resolve_expression(emotion), _AVATAR_SIZE_PX).tobytes()
            for emotion, frames in _LOOP_BY_EMOTION.items()
        }
        for emotion, image_bytes in images_by_emotion.items():
            for other_emotion, other_bytes in images_by_emotion.items():
                if other_emotion is not emotion:
                    self.assertNotEqual(image_bytes, other_bytes, f"{emotion} looks identical to {other_emotion}")

    def test_fears_own_decorations_never_include_the_exclamation_mark(self) -> None:
        """Fear passed through as surprise once, borrowing its exclamation
        mark and wide eyes — a regression this guards against."""
        for pose in FEAR_FRAMES:
            for shape in pose.extra:
                self.assertNotIn(shape, EXCLAMATION_MARK)


if __name__ == "__main__":
    unittest.main()
