"""Decides what parsing step one incoming user turn needs."""

from app.conversation import Conversation
from app.intents.models import ParseResult
from app.intents.parser import IntentParser
from app.intents.wake_word import strip_wake_word

_TEXT_JOIN_SEPARATOR = " "


async def resolve_turn(conversation: Conversation, parser: IntentParser, text: str) -> ParseResult:
    """Parse `text`, continuing any pending intent or starting a fresh one.

    A pending intent is continued by re-parsing every user utterance said
    since it started, plus this new one, so a stateless `IntentParser` still
    sees the full context (e.g. the model keyword from the first message).
    """
    stripped = strip_wake_word(text)
    if conversation.pending is None:
        return await parser.parse(stripped, conversation.history())
    combined_text = _combine_with_prior_turns(conversation, stripped)
    return await parser.parse(combined_text, conversation.history())


def _combine_with_prior_turns(conversation: Conversation, text: str) -> str:
    """Join every prior user utterance with `text`, oldest first."""
    prior_user_texts = [turn.text for turn in conversation.history() if turn.speaker == "user"]
    return _TEXT_JOIN_SEPARATOR.join([*prior_user_texts, text])
