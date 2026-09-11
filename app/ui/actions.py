"""What happens when the user does something: send, toggle mic, toggle camera,
or quit. Behavior only — `ui/app.py` owns widget composition and lifecycle.
"""

from app.errors import SpeechRecognitionError, SynthesisError
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
)
from app.ui.widgets.status_bar import MIC_RECORDING
from app.workers.camera_worker import CameraCallbacks, CameraSample, CameraTiming, CameraWorker
from app.workers.listening import listen
from app.workers.speaking import speak


class JarvisActions:
    """Mixin holding `JarvisApp`'s user-triggered command handlers."""

    def on_send(self) -> None:
        """Send the entry's current text through the same path as speech."""
        text = self.input_row.get_text().strip()
        self.input_row.clear()
        if text:
            self._submit_text(text)

    def on_mic_toggle(self) -> None:
        """Start recording on the first press, stop and transcribe on the second."""
        if self._recording:
            self._recording = False
            self.input_row.set_mic_processing()
            self.input_row.set_input_enabled(False)
            self._bridge.submit(self._finish_recording())
        else:
            self._player.stop()
            self._recorder.start()
            self._recording = True
            self.avatar_pane.set_state(AvatarState.LISTENING)
            self.input_row.set_mic_recording(True)
            self.status_bar.set_mic_state(MIC_RECORDING)

    def on_camera_toggle(self) -> None:
        """Turn webcam emotion sampling on or off (Ctrl+E or the card button, §15)."""
        self._camera_enabled = not self._camera_enabled
        if self._camera_enabled:
            self._start_camera_worker()
            self.camera_toggle_button.configure(text=strings.CAMERA_TOGGLE_ON)
        else:
            self._camera_worker.stop()
            self.camera_preview.show_disabled()
            self.camera_toggle_button.configure(text=strings.CAMERA_TOGGLE_OFF)

    def on_quit(self) -> None:
        """Release the camera and audio handles, then close the window."""
        self.destroy_app()

    async def _finish_recording(self) -> None:
        """Transcribe the just-stopped recording and route it like typed text."""
        try:
            text = await listen(self._recorder, self._stt)
        except SpeechRecognitionError as exc:
            self._dispatch.put(ErrorOccurred(str(exc)))
            text = ""
        self._dispatch.put(TranscriptReady(text))

    def _submit_text(self, text: str) -> None:
        """Log the user's turn and hand it to the orchestrator in the background."""
        self.conversation_view.append_turn(Speaker.USER, text)
        self.avatar_pane.set_state(AvatarState.THINKING)
        self._bridge.submit(self._run_turn(text))

    async def _run_turn(self, text: str) -> None:
        """Resolve one turn end-to-end and post its reply back to the UI."""
        reply = await self._orchestrator.handle_user_text(text)
        self._dispatch.put(AssistantReplied(reply))

    def _start_speaking(self, text: str) -> None:
        """Show the speaking state and synthesize `text` in the background."""
        self.avatar_pane.set_state(AvatarState.SPEAKING)
        self._bridge.submit(self._speak(text))

    async def _speak(self, text: str) -> None:
        """Play `text` back, reporting a failure but always signaling completion."""
        try:
            await speak(self._tts, self._player, text)
        except SynthesisError as exc:
            self._dispatch.put(ErrorOccurred(str(exc)))
        self._dispatch.put(SpeakingFinished())

    def _start_camera_worker(self) -> None:
        """(Re)start the webcam sampling loop as a background OS thread."""
        timing = CameraTiming(self._camera_frame_interval_seconds, self._emotion_interval_seconds)
        callbacks = CameraCallbacks(on_sample=self._on_camera_sample, on_error=self._on_camera_error)
        self._camera_worker = CameraWorker(self._camera, self._emotion_detector, timing, callbacks)
        self._camera_worker.start()

    def _on_camera_sample(self, sample: CameraSample | None) -> None:
        """Forward one webcam sample from the worker thread to the UI thread."""
        self._dispatch.put(CameraSampleReady(sample))

    def _on_camera_error(self, detail: str) -> None:
        """Forward the worker thread's terminal failure to the UI thread."""
        self._dispatch.put(CameraFailed(detail))
