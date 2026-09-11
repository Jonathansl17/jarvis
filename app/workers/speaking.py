"""Synthesizes and plays back speech off the event loop."""

import asyncio
import re

from app.speech.tts.player import AudioPlayer
from app.speech.tts.protocol import TextToSpeech

# Emoji and pictographs, which the voice would otherwise read out by name.
_UNSPOKEN_SYMBOLS = re.compile(r"[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]")


def strip_unspoken_symbols(text: str) -> str:
    """Remove emoji and pictographs so only words reach the synthesizer."""
    return _UNSPOKEN_SYMBOLS.sub("", text).strip()


async def speak(tts: TextToSpeech, player: AudioPlayer, text: str) -> float:
    """Synthesize `text` and play it back; return its playback duration in seconds."""
    samples = await asyncio.to_thread(tts.synthesize, strip_unspoken_symbols(text))
    return await asyncio.to_thread(player.play, samples)
