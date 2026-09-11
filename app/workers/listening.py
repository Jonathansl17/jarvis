"""Stops a recording and transcribes it off the event loop."""

import asyncio

from app.speech.stt.protocol import SpeechToText
from app.speech.stt.recorder import AudioRecorder


async def listen(recorder: AudioRecorder, stt: SpeechToText) -> str:
    """Stop `recorder` and return the transcript of what it captured."""
    audio = await asyncio.to_thread(recorder.stop)
    return await asyncio.to_thread(stt.transcribe, audio)
