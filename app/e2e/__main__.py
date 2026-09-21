"""Entry point: `python -m app.e2e [--typed] [--seed N] [--interval S]`."""

import argparse
import random
import sys
from dataclasses import replace

from app.e2e.driver import DriverTiming, SmokeDriver
from app.e2e.health import CountingDispatchQueue, HealthMonitor
from app.e2e.prompts import load_prompt_sections, pick_one_per_model
from app.e2e.speech_injection import ScriptedSpeechRecorder
from app.main import create_app
from app.ui.app import JarvisApp
from app.ui.bridge import EventLoopThread
from app.ui.collaborators import RuntimeCollaborators

_DEFAULT_TURN_INTERVAL_SECONDS = 16.0
_DEFAULT_MIC_HOLD_SECONDS = 4.0
_DEFAULT_STALL_SECONDS = 0.4
_STARTUP_DELAY_SECONDS = 8.0
_EXIT_FAILURE = 1


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="python -m app.e2e", description=__doc__)
    parser.add_argument("--typed", action="store_true", help="type each sentence instead of speaking it")
    parser.add_argument("--seed", type=int, default=None, help="seed for the per-model random pick")
    parser.add_argument("--interval", type=float, default=_DEFAULT_TURN_INTERVAL_SECONDS,
                        help="seconds between turns (default %(default)s)")
    parser.add_argument("--stall", type=float, default=_DEFAULT_STALL_SECONDS,
                        help="main-thread silence counted as a stall, in seconds (default %(default)s)")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    """Build the app exactly like `python -m app`, with the smoke test's probes wired in."""
    args = _parse_args(argv)
    seed = args.seed if args.seed is not None else random.randrange(sys.maxsize)
    prompts = pick_one_per_model(load_prompt_sections(), random.Random(seed))
    print(f"seed={seed} mode={'typed' if args.typed else 'voice'} turns={len(prompts)}", flush=True)

    bridge = EventLoopThread()
    bridge.start()
    dispatch = CountingDispatchQueue()
    collaborators = bridge.submit(create_app()).result()
    recorder = None if args.typed else ScriptedSpeechRecorder(collaborators.speech.tts)
    speech = collaborators.speech if recorder is None else replace(collaborators.speech, recorder=recorder)
    app = JarvisApp(
        dialogue=collaborators.dialogue,
        speech=speech,
        emotion=collaborators.emotion,
        runtime=RuntimeCollaborators(bridge=bridge, dispatch=dispatch, options=collaborators.options),
    )
    monitor = HealthMonitor(app.root.after, app.root.after_idle, dispatch, args.stall)
    driver = SmokeDriver(app, monitor, DriverTiming(args.interval, _DEFAULT_MIC_HOLD_SECONDS), _print_line)
    driver.run(prompts, recorder, _STARTUP_DELAY_SECONDS)
    app.run()
    return 0 if driver.passed else _EXIT_FAILURE


def _print_line(line: str) -> None:
    print(line, flush=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
