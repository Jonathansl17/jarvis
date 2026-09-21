"""The scripted recorder must still drive the real stream and hand back the
queued sentence as 16 kHz audio, or the real capture when nothing is queued."""

import unittest

import numpy as np

from app.constants import PIPER_SAMPLE_RATE_HZ, STT_SAMPLE_RATE_HZ
from app.e2e.speech_injection import ScriptedSpeechRecorder


class _FakeStream:
    def __init__(self, callback) -> None:
        self.callback = callback
        self.started = 0
        self.stopped = 0

    def start(self) -> None:
        self.started += 1

    def stop(self) -> None:
        self.stopped += 1

    def close(self) -> None:
        pass


class _FakeTts:
    def __init__(self) -> None:
        self.requests: list[str] = []

    def synthesize(self, text: str):
        self.requests.append(text)
        return np.ones(PIPER_SAMPLE_RATE_HZ, dtype=np.float32)  # one second of "speech"


class ScriptedSpeechRecorderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.streams: list[_FakeStream] = []
        self.tts = _FakeTts()

        def open_stream(callback):
            stream = _FakeStream(callback)
            self.streams.append(stream)
            return stream

        self.recorder = ScriptedSpeechRecorder(self.tts, open_stream=open_stream)

    def test_queued_sentence_comes_back_as_one_second_at_whisper_rate(self) -> None:
        self.recorder.say_next("hola")
        self.recorder.start()
        audio = self.recorder.stop()
        self.assertEqual(self.tts.requests, ["hola"])
        self.assertEqual(len(audio), STT_SAMPLE_RATE_HZ)
        self.assertEqual(audio.dtype, np.float32)
        self.assertEqual((self.streams[0].started, self.streams[0].stopped), (1, 1))

    def test_without_a_queued_sentence_the_real_capture_is_returned(self) -> None:
        self.recorder.start()
        self.streams[0].callback(np.full((8, 1), 0.5, dtype=np.float32), 8, None, None)
        audio = self.recorder.stop()
        self.assertEqual(self.tts.requests, [])
        self.assertTrue(np.all(audio == 0.5))

    def test_a_queued_sentence_is_used_once(self) -> None:
        self.recorder.say_next("una vez")
        self.recorder.start()
        self.recorder.stop()
        self.recorder.start()
        self.assertEqual(len(self.recorder.stop()), 0)
