"""Entry point: `python -m app.e2e`. No options: every run speaks one random
sentence per model and prints the seed it picked with."""

import random
import sys

from app.e2e.driver import DriverTiming, SmokeDriver
from app.e2e.health import CountingDispatchQueue, HealthMonitor
from app.e2e.prompts import load_prompt_sections, pick_one_per_model
from app.e2e.speech_injection import ScriptedSpeechRecorder
from app.main import create_app
from app.ui.app import JarvisApp
from app.ui.bridge import EventLoopThread
from app.ui.collaborators import RuntimeCollaborators, SpeechCollaborators

_TURN_INTERVAL_SECONDS = 16.0
_MIC_HOLD_SECONDS = 4.0
_STALL_SECONDS = 0.4
_STARTUP_DELAY_SECONDS = 8.0
_EXIT_FAILURE = 1


def main() -> int:
    """Build the app exactly like `python -m app`, with the smoke test's probes wired in."""
    seed = random.randrange(sys.maxsize)
    prompts = pick_one_per_model(load_prompt_sections(), random.Random(seed))
    print(f"seed={seed} turns={len(prompts)}", flush=True)

    bridge = EventLoopThread()
    bridge.start()
    dispatch = CountingDispatchQueue()
    collaborators = bridge.submit(create_app()).result()
    speech = collaborators.speech
    recorder = ScriptedSpeechRecorder(speech.tts)
    app = JarvisApp(
        dialogue=collaborators.dialogue,
        speech=SpeechCollaborators(recorder=recorder, stt=speech.stt, tts=speech.tts, player=speech.player),
        emotion=collaborators.emotion,
        runtime=RuntimeCollaborators(bridge=bridge, dispatch=dispatch, options=collaborators.options),
    )
    monitor = HealthMonitor(app.root.after, app.root.after_idle, dispatch, _STALL_SECONDS)
    driver = SmokeDriver(app, monitor, DriverTiming(_TURN_INTERVAL_SECONDS, _MIC_HOLD_SECONDS), _print_line)
    driver.run(prompts, recorder, _STARTUP_DELAY_SECONDS)
    app.run()
    return 0 if driver.passed else _EXIT_FAILURE


def _print_line(line: str) -> None:
    print(line, flush=True)


if __name__ == "__main__":
    sys.exit(main())
