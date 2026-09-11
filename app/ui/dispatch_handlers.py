"""What happens when a message drained from the bridge queue arrives.

One method per `ui.messages` type; `ui/app.py`'s poll timer dispatches into
this mixin by message type.
"""

from app.dialogue.strings import EMPTY_TRANSCRIPT_TEXT
from app.intents.models import Speaker
from app.ui import strings
from app.ui.avatar.spec import AvatarState
from app.ui.messages import (
    AssistantReplied,
    CameraFailed,
    CameraSampleReady,
    ErrorOccurred,
    SpeakingFinished,
    TranscriptReady,
    UiMessage,
)
from app.ui.notice_parsing import extract_fallback_model
from app.ui.widgets.status_bar import MIC_IDLE

_DISPATCH_BY_TYPE = {
    TranscriptReady: "_on_transcript_ready",
    AssistantReplied: "_on_assistant_replied",
    CameraSampleReady: "_on_camera_sample_ready",
    ErrorOccurred: "_on_error_occurred",
    SpeakingFinished: "_on_speaking_finished",
    CameraFailed: "_on_camera_failed",
}


class JarvisDispatchHandlers:
    """Mixin holding `JarvisApp`'s per-message-type background event handlers."""

    def dispatch(self, message: UiMessage) -> None:
        """Route `message` to the handler named for its type."""
        getattr(self, _DISPATCH_BY_TYPE[type(message)])(message)

    def _on_transcript_ready(self, message: TranscriptReady) -> None:
        """Re-enable input and submit the transcript, or report an empty one."""
        self.input_row.set_mic_recording(False)
        self.input_row.set_input_enabled(True)
        self.status_bar.set_mic_state(MIC_IDLE)
        if message.text:
            self._submit_text(message.text)
        else:
            self.conversation_view.append_turn(Speaker.ASSISTANT, EMPTY_TRANSCRIPT_TEXT)
            self.avatar_pane.set_state(AvatarState.IDLE)

    def _on_assistant_replied(self, message: AssistantReplied) -> None:
        """Update the IA status field on a model fallback, then speak the reply.

        System notices never reach the chat: they are Gemini model-fallback
        text meant for the status strip's IA field, not a conversation turn.
        """
        if message.reply.system_notice:
            model = extract_fallback_model(message.reply.system_notice)
            if model is not None:
                self.status_bar.set_ia_state(model)
        self.conversation_view.append_turn(Speaker.ASSISTANT, message.reply.text)
        if self._tts_enabled:
            self._start_speaking(message.reply.text)
        else:
            self.avatar_pane.finish_reply()

    def _on_speaking_finished(self, _message: SpeakingFinished) -> None:
        """Return the avatar to idle once TTS playback ends, hopping first if
        the mirrored emotion the user is showing is happy or surprise."""
        self.avatar_pane.finish_reply()

    def _on_camera_sample_ready(self, message: CameraSampleReady) -> None:
        """Refresh the preview and, above the confidence cutoff, the avatar.

        The status strip always mirrors the camera card's own emotion word
        exactly. No face means no emotion: the avatar and the tone go back
        to neutral instead of keeping the last reading.
        """
        self.camera_preview.update_sample(message.sample)
        sample = message.sample
        if sample is None:
            return
        self.status_bar.set_emotion_reading(sample.reading)
        emotion = sample.reading[0] if sample.reading is not None else None
        self._conversation.set_last_emotion(emotion)
        self.avatar_pane.set_emotion(emotion)

    def _on_error_occurred(self, message: ErrorOccurred) -> None:
        """Report a background failure as a short red line in the status strip.

        Real errors (API unreachable, mic failure) never reach the chat.
        """
        self.status_bar.set_error(message.detail)
        self.input_row.set_mic_recording(False)
        self.status_bar.set_mic_state(MIC_IDLE)

    def _on_camera_failed(self, message: CameraFailed) -> None:
        """Reflect a dead camera worker everywhere its state is shown.

        Keeps the toggle button, the camera card, and the status strip as
        one source of truth: `self._camera_enabled` — never just the
        preview going quiet with the button still claiming "ON".
        """
        self._camera_enabled = False
        self.camera_toggle_button.configure(text=strings.CAMERA_TOGGLE_OFF)
        self.camera_preview.show_disabled()
        self.status_bar.set_error(message.detail)
