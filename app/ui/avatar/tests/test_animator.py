"""Regression tests for the idle animator's per-emotion loop switching."""

import unittest

from app.emotion.protocol import Emotion
from app.ui.avatar.animator import AvatarAnimator
from app.ui.avatar.idle_frames import IDLE_BOUNCE_START_INDEX


def _no_op_schedule(duration_ms: int, callback) -> object:
    return object()


def _identity_render(state, frame_index, emotion):
    return frame_index


class IdleLoopSwitchingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.animator = AvatarAnimator(_no_op_schedule, _identity_render, lambda image: None)

    def test_default_idle_loop_is_breathing(self) -> None:
        self.assertEqual(self.animator._frame_index, 0)

    def test_happy_switches_to_its_own_bounce_loop(self) -> None:
        self.animator.set_emotion(Emotion.HAPPY)
        self.assertEqual(self.animator._frame_index, IDLE_BOUNCE_START_INDEX)

    def test_bounce_loop_wraps_after_two_frames(self) -> None:
        self.animator.set_emotion(Emotion.HAPPY)
        self.animator._advance(400)
        self.assertEqual(self.animator._frame_index, IDLE_BOUNCE_START_INDEX + 1)
        self.animator._advance(400)
        self.assertEqual(self.animator._frame_index, IDLE_BOUNCE_START_INDEX)

    def test_an_event_resumes_the_active_emotion_loop_not_breathing(self) -> None:
        self.animator.set_emotion(Emotion.HAPPY)
        self.animator._start_event(0, 1)  # simulate a spliced-in blink
        self.animator._advance_event()  # exhausts it -> should resume happy's loop
        self.assertEqual(self.animator._frame_index, IDLE_BOUNCE_START_INDEX)

    def test_an_emotion_without_its_own_loop_falls_back_to_breathing(self) -> None:
        self.animator.set_emotion(Emotion.HAPPY)
        self.animator.set_emotion(Emotion.SAD)
        self.assertEqual(self.animator._frame_index, 0)


if __name__ == "__main__":
    unittest.main()
