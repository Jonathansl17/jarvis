"""Regression tests for the idle animator's per-emotion loop switching and
its reaction transition on emotion change."""

import unittest

from app.emotion.protocol import Emotion
from app.ui.avatar.animator import AvatarAnimator
from app.ui.avatar.idle_frames import IDLE_HAPPY_START_INDEX, IDLE_TRANSITION_START_INDEX
from app.ui.avatar.loops import HAPPY_FRAMES


def _no_op_schedule(duration_ms: int, callback) -> object:
    return object()


def _identity_render(state, frame_index, emotion):
    return frame_index


def _settle(animator: AvatarAnimator) -> None:
    """Fast-forward past any event (blink/wave/hop/transition) currently
    playing, landing on the active idle loop's start frame."""
    while animator._playing_event:
        animator._advance_event()


class IdleLoopSwitchingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.animator = AvatarAnimator(_no_op_schedule, _identity_render, lambda image: None)

    def test_default_idle_loop_is_breathing(self) -> None:
        self.assertEqual(self.animator._frame_index, 0)

    def test_setting_an_emotion_plays_the_reaction_transition_first(self) -> None:
        self.animator.set_emotion(Emotion.HAPPY)
        self.assertEqual(self.animator._frame_index, IDLE_TRANSITION_START_INDEX)
        self.assertTrue(self.animator._playing_event)

    def test_happy_settles_into_its_own_bounce_loop_after_the_transition(self) -> None:
        self.animator.set_emotion(Emotion.HAPPY)
        _settle(self.animator)
        self.assertEqual(self.animator._frame_index, IDLE_HAPPY_START_INDEX)

    def test_happy_loop_wraps_after_its_full_frame_count(self) -> None:
        self.animator.set_emotion(Emotion.HAPPY)
        _settle(self.animator)
        for _ in range(len(HAPPY_FRAMES)):
            self.animator._advance(400)
        self.assertEqual(self.animator._frame_index, IDLE_HAPPY_START_INDEX)

    def test_an_event_resumes_the_active_emotion_loop_not_breathing(self) -> None:
        self.animator.set_emotion(Emotion.HAPPY)
        _settle(self.animator)
        self.animator._start_event(0, 1)  # simulate a spliced-in blink
        self.animator._advance_event()  # exhausts it -> should resume happy's loop
        self.assertEqual(self.animator._frame_index, IDLE_HAPPY_START_INDEX)

    def test_repeating_the_same_emotion_does_not_replay_the_transition(self) -> None:
        self.animator.set_emotion(Emotion.HAPPY)
        _settle(self.animator)
        self.animator.set_emotion(Emotion.HAPPY)
        self.assertFalse(self.animator._playing_event)
        self.assertEqual(self.animator._frame_index, IDLE_HAPPY_START_INDEX)

    def test_neutral_has_no_own_loop_and_falls_back_to_breathing(self) -> None:
        self.animator.set_emotion(Emotion.HAPPY)
        _settle(self.animator)
        self.animator.set_emotion(Emotion.NEUTRAL)
        _settle(self.animator)
        self.assertEqual(self.animator._frame_index, 0)


if __name__ == "__main__":
    unittest.main()
