"""Regression tests for the crash on `snd_pcm_close`: playback must reuse one
open output stream, never closing it between replies, and `stop()` must cut
a playback between blocks."""

import threading
import unittest

import numpy as np

from app.constants import PLAYBACK_BLOCK_FRAMES
from app.speech.tts.player import AudioPlayer


class _FakeStream:
    def __init__(self, on_write=None) -> None:
        self.writes: list[int] = []
        self.closed = False
        self._on_write = on_write

    def write(self, block) -> None:
        self.writes.append(len(block))
        if self._on_write is not None:
            self._on_write(self)

    def stop(self) -> None:
        pass

    def close(self) -> None:
        self.closed = True


class _Factory:
    def __init__(self, stream: _FakeStream) -> None:
        self.stream = stream
        self.calls = 0

    def __call__(self) -> _FakeStream:
        self.calls += 1
        return self.stream


class AudioPlayerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stream = _FakeStream()
        self.factory = _Factory(self.stream)
        self.player = AudioPlayer(open_stream=self.factory)

    def test_consecutive_plays_share_one_stream_and_never_close_it(self) -> None:
        samples = np.zeros(PLAYBACK_BLOCK_FRAMES * 3, dtype=np.float32)
        self.player.play(samples)
        self.player.play(samples)
        self.assertEqual(self.factory.calls, 1)
        self.assertFalse(self.stream.closed)
        self.assertEqual(self.stream.writes, [PLAYBACK_BLOCK_FRAMES] * 6)

    def test_play_writes_the_tail_block_and_returns_the_full_duration(self) -> None:
        samples = np.zeros(PLAYBACK_BLOCK_FRAMES + 100, dtype=np.float32)
        duration = self.player.play(samples)
        self.assertEqual(self.stream.writes, [PLAYBACK_BLOCK_FRAMES, 100])
        self.assertAlmostEqual(duration, len(samples) / 22050)

    def test_stop_cuts_playback_between_blocks(self) -> None:
        stream = _FakeStream()
        player = AudioPlayer(open_stream=_Factory(stream))
        stream._on_write = lambda _stream: player.stop()
        player.play(np.zeros(PLAYBACK_BLOCK_FRAMES * 4, dtype=np.float32))
        self.assertEqual(len(stream.writes), 1)
        self.assertFalse(stream.closed)

    def test_a_new_play_interrupts_the_one_in_progress(self) -> None:
        first_started = threading.Event()
        release_first = threading.Event()

        def block_first_write(_stream: _FakeStream) -> None:
            if not first_started.is_set():
                first_started.set()
                release_first.wait(timeout=2)

        stream = _FakeStream(on_write=block_first_write)
        player = AudioPlayer(open_stream=_Factory(stream))
        long_samples = np.zeros(PLAYBACK_BLOCK_FRAMES * 10, dtype=np.float32)
        first = threading.Thread(target=player.play, args=(long_samples,))
        first.start()
        first_started.wait(timeout=2)

        second = threading.Thread(target=player.play, args=(np.zeros(PLAYBACK_BLOCK_FRAMES, dtype=np.float32),))
        second.start()
        release_first.set()
        first.join(timeout=2)
        second.join(timeout=2)
        # First play wrote one block then yielded; second wrote its single block.
        self.assertEqual(len(stream.writes), 2)
        self.assertFalse(stream.closed)

    def test_close_releases_the_stream_once(self) -> None:
        self.player.play(np.zeros(10, dtype=np.float32))
        self.player.close()
        self.assertTrue(self.stream.closed)
        self.player.close()
        self.assertEqual(self.factory.calls, 1)
