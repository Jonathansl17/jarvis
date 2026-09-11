"""Decides what parsing step one incoming user turn needs."""

from app.conversation import Conversation
from app.intents.models import NeedsInput, ParseResult, PendingIntent, ResolvedIntent, Speaker
from app.intents.parser import IntentParser
from app.intents.rules.base import parse_bare_number
from app.intents.wake_word import strip_wake_word

_TEXT_JOIN_SEPARATOR = " "


async def resolve_turn(conversation: Conversation, parser: IntentParser, text: str) -> ParseResult:
    """Parse `text`, continuing any pending intent or starting a fresh one.

    A pending intent is continued by re-parsing every user utterance said
    since *it* started, plus this new one, so a stateless `IntentParser`
    still sees the full context (e.g. the model keyword from the first
    message) without picking up an unrelated number left over from an
    earlier, already-resolved request.
    """
    stripped = strip_wake_word(text)
    if conversation.pending is None:
        return await parser.parse(stripped, conversation.history())
    pending = conversation.pending
    combined_text = _combine_with_pending_turns(conversation, stripped)
    result = await parser.parse(combined_text, conversation.history())
    return _fill_from_bare_answer(pending, stripped, result)


def _combine_with_pending_turns(conversation: Conversation, text: str) -> str:
    """Join `text` with every user utterance since the pending intent began.

    `conversation.add_turn` already recorded the turn `text` came from, as
    the last entry of `turns_since_pending`, so it is excluded here and
    appended once, wake-word-stripped, instead of twice.
    """
    earlier_turns = conversation.turns_since_pending()[:-1]
    prior_user_texts = [turn.text for turn in earlier_turns if turn.speaker == Speaker.USER]
    return _TEXT_JOIN_SEPARATOR.join([*prior_user_texts, text])


def _fill_from_bare_answer(pending: PendingIntent, text: str, result: ParseResult) -> ParseResult:
    """Take a bare numeric `text` literally for the field it was just asked about.

    Only applies when re-parsing the combined text still missed that exact
    field, so a short answer like "2" to "¿para cuántos días...?" is not
    lost just because the question itself had no keyword to anchor a search.
    """
    if not isinstance(result, NeedsInput) or not pending.missing:
        return result
    field = pending.missing[0]
    if field not in result.missing:
        return result
    value = parse_bare_number(text)
    if value is None:
        return result
    fields = {**result.fields, field: int(value) if value.is_integer() else value}
    still_missing = [name for name in result.missing if name != field]
    if still_missing:
        return NeedsInput(model_name=result.model_name, fields=fields, missing=still_missing)
    return ResolvedIntent(model_name=result.model_name, fields=fields)
