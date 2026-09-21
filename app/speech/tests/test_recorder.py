"""Regression tests: recordings reuse one open input stream, capturing blocks
only while recording, and never close it between recordings."""

import unittest

import numpy as np

from app.errors import SpeechRecognitionError
from app.speech.stt.recorder import AudioRecorder


class _FakeStream:
    def __init__(self, callback) -> None:
        self.callback = callback
        self.started = 0
        self.stopped = 0
        self.closed = False

    def start(self) -> None:
        self.started += 1

    def stop(self) -> None:
        self.stopped += 1

    def close(self) -> None:
        self.closed = True


class _Factory:
    def __init__(self) -> None:
        self.streams: list[_FakeStream] = []

    def __call__(self, callback) -> _FakeStream:
        stream = _FakeStream(callback)
        self.streams.append(stream)
        return stream


def _feed(stream: _FakeStream, value: float) -> None:
    stream.callback(np.full((4, 1), value, dtype=np.float32), 4, None, None)


class AudioRecorderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.factory = _Factory()
        self.recorder = AudioRecorder(open_stream=self.factory)

    def test_two_recordings_share_one_stream_that_is_never_closed(self) -> None:
        self.recorder.start()
        stream = self.factory.streams[0]
        _feed(stream, 1.0)
        first = self.recorder.stop()
        self.recorder.start()
        _feed(stream, 2.0)
        second = self.recorder.stop()
        self.assertEqual(len(self.factory.streams), 1)
        self.assertFalse(stream.closed)
        self.assertEqual((stream.started, stream.stopped), (2, 2))
        self.assertTrue(np.all(first == 1.0) and np.all(second == 2.0))
        self.assertEqual(first.shape, (4,))

    def test_blocks_arriving_while_stopped_are_dropped(self) -> None:
        self.recorder.start()
        stream = self.factory.streams[0]
        self.recorder.stop()
        _feed(stream, 9.0)
        self.recorder.start()
        self.assertEqual(len(self.recorder.stop()), 0)

    def test_start_twice_and_stop_without_start_raise(self) -> None:
        with self.assertRaises(SpeechRecognitionError):
            self.recorder.stop()
        self.recorder.start()
        with self.assertRaises(SpeechRecognitionError):
            self.recorder.start()

    def test_close_releases_the_stream(self) -> None:
        self.recorder.start()
        self.recorder.close()
        self.assertTrue(self.factory.streams[0].closed)
        self.recorder.close()
