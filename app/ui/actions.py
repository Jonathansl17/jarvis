"""Key bindings and message handlers for `JarvisApp`, kept out of app.py to
stay under the file's size ceiling; behavior only, no widget composition.
"""

from textual.widgets import Input

from app.constants import EMOTION_LOW_CONFIDENCE_THRESHOLD
from app.dialogue.strings import EMPTY_TRANSCRIPT_TEXT
from app.emotion.protocol import Emotion
from app.errors import SpeechRecognitionError, SynthesisError
from app.intents.models import Speaker
from app.ui.frames import AvatarState
from app.ui.messages import (
    AssistantReplied,
    EmotionUpdated,
    ErrorOccurred,
    TranscriptReady,
)
from app.ui.widgets.avatar_pane import AvatarPane
from app.ui.widgets.conversation_log import ConversationLog
from app.ui.widgets.status_bar import MIC_GRABANDO, MIC_LISTO, MIC_PROCESANDO, StatusBar
from app.workers.emotion_sampling import sample_emotion_forever
from app.workers.listening import listen
from app.workers.speaking import speak

_EMOTION_WORKER_GROUP = "emotion"
_LISTENING_WORKER_GROUP = "listening"
_TURN_WORKER_GROUP = "turn"
_SPEAKING_WORKER_GROUP = "speaking"
_SPACE = " "


class JarvisActions:
    """Mixin holding `JarvisApp`'s bindings, actions, and message handlers."""

    def action_toggle_recording(self) -> None:
        """Start recording on the first press, stop and transcribe on the second.

        While the user is typing, space keeps its normal meaning.
        """
        input_line = self.query_one("#input-line", Input)
        if input_line.value and not self._recording:
            input_line.insert_text_at_cursor(_SPACE)
            return
        if self._recording:
            self._recording = False
            self.query_one(StatusBar).set_mic_state(MIC_PROCESANDO)
            self.query_one("#input-line").disabled = True
            self.run_worker(self._finish_recording(), group=_LISTENING_WORKER_GROUP)
        else:
            self._recorder.start()
            self._recording = True
            self.query_one(AvatarPane).set_state(AvatarState.LISTENING)
            self.query_one(StatusBar).set_mic_state(MIC_GRABANDO)

    def action_toggle_camera(self) -> None:
        """Turn webcam emotion sampling on or off, per the `e` key (§9)."""
        self._camera_enabled = not self._camera_enabled
        if self._camera_enabled:
            self._start_emotion_worker()
        else:
            self.workers.cancel_group(self, _EMOTION_WORKER_GROUP)
            self.query_one(StatusBar).set_emotion(None, None)

    def on_input_submitted(self, message: Input.Submitted) -> None:
        """Send typed text through the same path as a transcribed utterance."""
        text = message.value.strip()
        self.query_one("#input-line").value = ""
        if text:
            self._submit_text(text)

    async def _finish_recording(self) -> None:
        """Transcribe the just-stopped recording and route it like typed text."""
        try:
            text = await listen(self._recorder, self._stt)
        except SpeechRecognitionError as exc:
            self.post_message(ErrorOccurred(str(exc)))
            text = ""
        self.post_message(TranscriptReady(text))

    def on_transcript_ready(self, message: TranscriptReady) -> None:
        """Re-enable input and submit the transcript, or report an empty one."""
        self.query_one(StatusBar).set_mic_state(MIC_LISTO)
        self.query_one("#input-line").disabled = False
        if message.text:
            self._submit_text(message.text)
        else:
            self.query_one(ConversationLog).append_turn(Speaker.ASSISTANT, EMPTY_TRANSCRIPT_TEXT)

    def _submit_text(self, text: str) -> None:
        """Log the user's turn and hand it to the orchestrator in the background."""
        self.query_one(ConversationLog).append_turn(Speaker.USER, text)
        self.query_one(AvatarPane).set_state(AvatarState.THINKING)
        self.run_worker(self._run_turn(text), group=_TURN_WORKER_GROUP)

    async def _run_turn(self, text: str) -> None:
        """Resolve one turn end-to-end and post its reply back to the UI."""
        reply = await self._orchestrator.handle_user_text(text)
        self.post_message(AssistantReplied(reply))

    def on_assistant_replied(self, message: AssistantReplied) -> None:
        """Log any fallback notice and the reply, then speak it if TTS is enabled."""
        log = self.query_one(ConversationLog)
        if message.reply.system_notice:
            log.append_turn(Speaker.SYSTEM, message.reply.system_notice)
        log.append_turn(Speaker.ASSISTANT, message.reply.text)
        if self._tts_enabled:
            self.run_worker(self._speak(message.reply.text), group=_SPEAKING_WORKER_GROUP)
        else:
            self.query_one(AvatarPane).set_state(AvatarState.IDLE)

    async def _speak(self, text: str) -> None:
        """Show the speaking state for exactly as long as playback lasts."""
        self.query_one(AvatarPane).set_state(AvatarState.SPEAKING)
        try:
            await speak(self._tts, self._player, text)
        except SynthesisError as exc:
            self.post_message(ErrorOccurred(str(exc)))
        self.query_one(AvatarPane).set_state(AvatarState.IDLE)

    def _start_emotion_worker(self) -> None:
        """(Re)start the webcam sampling loop as a background worker."""
        self.run_worker(
            sample_emotion_forever(
                self._camera, self._emotion_detector, self._emotion_interval_seconds, self._on_emotion
            ),
            group=_EMOTION_WORKER_GROUP,
        )

    def _on_emotion(self, reading: tuple[Emotion, float] | None) -> None:
        """Forward one webcam sample from the worker loop to the UI thread."""
        self.post_message(EmotionUpdated(reading))

    def on_emotion_updated(self, message: EmotionUpdated) -> None:
        """Update the status badge and, above the confidence cutoff, the avatar."""
        if message.reading is None:
            return
        emotion, confidence = message.reading
        self.query_one(StatusBar).set_emotion(emotion.value, confidence)
        if confidence >= EMOTION_LOW_CONFIDENCE_THRESHOLD:
            self._conversation.set_last_emotion(emotion)
            self.query_one(AvatarPane).set_emotion(emotion)

    def on_error_occurred(self, message: ErrorOccurred) -> None:
        """Report a background failure as a SYS log line."""
        self.query_one(ConversationLog).append_turn(Speaker.SYSTEM, message.detail)
