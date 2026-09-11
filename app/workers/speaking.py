"""Synthesizes and plays back speech off the event loop."""

import asyncio

from app.speech.tts.player import AudioPlayer
from app.speech.tts.protocol import TextToSpeech


async def speak(tts: TextToSpeech, player: AudioPlayer, text: str) -> float:
    """Synthesize `text` and play it back; return its playback duration in seconds."""
    samples = await asyncio.to_thread(tts.synthesize, text)
    return await asyncio.to_thread(player.play, samples)
