"""Coordinates one user turn end-to-end: parse → predict → tone-adjust."""

from app.api_client.protocol import PredictionClient
from app.conversation import Conversation
from app.dialogue.missing_field_prompts import build_missing_field_question
from app.dialogue.reply import AssistantReply
from app.dialogue.reply_builder import build_prediction_reply
from app.dialogue.strings import NOT_UNDERSTOOD_TEXT, PREDICTION_ERROR_TEXT
from app.dialogue.turn_resolution import resolve_turn
from app.emotion.tone_adapter import ToneAdapter
from app.errors import IntentParsingError, PredictionRequestError
from app.intents.models import NeedsInput, ParseResult, ResolvedIntent, Turn
from app.intents.parser import IntentParser

_USER_SPEAKER = "user"
_ASSISTANT_SPEAKER = "assistant"


class DialogueOrchestrator:
    """Runs the parse/predict/tone-adjust pipeline shared by voice and text input."""

    def __init__(
        self,
        intent_parser: IntentParser,
        prediction_client: PredictionClient,
        tone_adapter: ToneAdapter,
        conversation: Conversation,
    ) -> None:
        self._intent_parser = intent_parser
        self._prediction_client = prediction_client
        self._tone_adapter = tone_adapter
        self._conversation = conversation

    async def handle_user_text(self, text: str) -> AssistantReply:
        """Record `text`, resolve it into a reply, and record that reply too."""
        self._conversation.add_turn(Turn(speaker=_USER_SPEAKER, text=text))
        reply = await self._resolve_and_reply(text)
        self._conversation.add_turn(Turn(speaker=_ASSISTANT_SPEAKER, text=reply.text))
        return reply

    async def _resolve_and_reply(self, text: str) -> AssistantReply:
        """Parse `text`, falling back to a not-understood reply on failure."""
        try:
            result = await resolve_turn(self._conversation, self._intent_parser, text)
        except IntentParsingError:
            self._conversation.set_pending(None)
            return self._reply(NOT_UNDERSTOOD_TEXT, awaiting_field=False, model_name=None)
        return await self._handle_parse_result(result)

    async def _handle_parse_result(self, result: ParseResult) -> AssistantReply:
        """Ask for the next missing field, or predict once everything is known."""
        if isinstance(result, NeedsInput):
            self._conversation.set_pending(result)
            question = build_missing_field_question(result.missing[0])
            return self._reply(question, awaiting_field=True, model_name=result.model_name)
        self._conversation.set_pending(None)
        return await self._predict_and_reply(result)

    async def _predict_and_reply(self, result: ResolvedIntent) -> AssistantReply:
        """Call the prediction API and phrase its response, or report failure."""
        try:
            body = await self._prediction_client.predict(result.model_name, result.fields)
        except PredictionRequestError:
            return self._reply(PREDICTION_ERROR_TEXT, awaiting_field=False, model_name=result.model_name)
        reply_text = build_prediction_reply(result.model_name, body)
        return self._reply(reply_text, awaiting_field=False, model_name=result.model_name)

    def _reply(self, text: str, *, awaiting_field: bool, model_name: str | None) -> AssistantReply:
        """Build an `AssistantReply`, applying the current tone adaptation."""
        toned_text = self._tone_adapter.apply(text, self._conversation.last_emotion)
        return AssistantReply(text=toned_text, awaiting_field=awaiting_field, model_name=model_name)
