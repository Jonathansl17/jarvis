# App

JarvisTEC, the desktop voice assistant of the project. Speech-to-text →
intent parsing (keyword rules, or Gemini when configured) → the REST API in
`api/` → tone-adjusted reply → text-to-speech, with a live webcam feed whose
detected emotion drives the tone of the replies and the expression of the
penguin avatar. Built with CustomTkinter, OpenCV and Pillow, runs on Linux,
Windows and macOS.

## Run

The app has its own virtual environment, separate from the one the
notebooks and the API share (see the root `README.md`). It needs Tk and
PortAudio from the system: `sudo apt install python3-tk libportaudio2` on
Ubuntu/Debian, `sudo pacman -S tk portaudio` on Arch, `sudo dnf install
python3-tkinter portaudio` on Fedora, `brew install python-tk portaudio` on
macOS; on Windows the python.org installer ships Tk and the `sounddevice`
wheel bundles PortAudio, so nothing extra is needed. The full table is in
the root `README.md`.

Linux and macOS, from the repository root:

```bash
python3 -m venv app/env
source app/env/bin/activate
pip install -r app/requirements.txt
cp app/.env.example app/.env   # fill in GEMINI_API_KEY (optional)
python -m app
```

Windows (PowerShell):

```powershell
py -m venv app\env
app\env\Scripts\activate
pip install -r app\requirements.txt
copy app\.env.example app\.env
python -m app
```

The API in `api/` must be running at `API_BASE_URL` (default
`http://localhost:8000`). The first run downloads the whisper `small` model
(about 500 MB) and the Spanish Piper voice (about 60 MB) into local caches.

## Configuration

Read once at startup by `app/config.py` (`pydantic-settings`) from `app/.env`
or the environment (`app/.env.example` is a starting point for `app/.env`):

- `GEMINI_API_KEY` — optional. Without it, intents are parsed by the keyword
  rules only. With it, Gemini is tried first and the rules are the fallback.
- `GEMINI_MODELS` — comma-separated Gemini models tried in order; a model
  whose quota is exhausted (429) or that was retired (404) is skipped for the
  rest of the session. Defaults to `gemini-3.6-flash,gemini-flash-lite-latest`.
  The status strip's `IA` field shows which one answered, or `reglas`.
- `API_BASE_URL` — base URL of the REST API.
- `MODELS_DIR` — folder with `facial_emotion_cnn.onnx` and the haar cascade.
  Defaults to the repository's `models/`.
- `PIPER_CACHE_DIR` — where the Piper voice is cached. Defaults to
  `app/.cache/piper/`.
- `CAMERA_ENABLED`, `TTS_ENABLED` — start with the webcam or the voice on or
  off. Default `true`.

## The window

Left column: the penguin avatar (idle, listening, thinking and speaking
states, one full-body expression and animation loop per detected emotion)
and the camera card with the mirrored webcam feed, the detected face boxed
and the emotion written under it. Right column: the conversation, with one
bubble per turn, and the input row with a single button that is the
microphone while the entry is empty, the send arrow once there is text, and
the red recording indicator while the mic is open. Bottom: the keyboard
hints and the status strip (MIC, EMO, API, STT, IA).

- `Enter` sends the typed text. `Ctrl+Space` or the MIC button starts a
  recording and stops it, then whisper transcribes it and the text follows
  the same path as typed input. Starting a recording interrupts the
  assistant's voice.
- `Ctrl+E` or the ON/OFF button on the camera card toggles the webcam.
  `Esc` quits.
- Right click or double click on a bubble copies its text.
- System notices (which Gemini model answered, fallbacks) never enter the
  chat: they go to the status strip.

Example sentences for every model, three each, are in `app/prompts.txt`.

## End-to-end smoke test

`app/e2e/` drives the real window — real API, whisper, Piper, webcam —
through one turn per model and fails if a turn goes unanswered or the Tk
main thread stalls. It exists because two bugs only showed up after several
consecutive turns (a PortAudio stream closed mid-playback aborting the
process, and leaked avatar timers starving the window until it stopped
repainting); unit tests never see either.

With the API running and the app's environment active, from the repository
root:

```bash
python -m app.e2e            # speaks one random sentence per model
python -m app.e2e --typed    # types them instead (no audio devices needed)
python -m app.e2e --seed 7   # replay a run: same random pick per model
```

Each run picks **one of the three sentences of every model at random** from
`app/prompts.txt` and prints the seed first, so a failing pick can be
replayed with `--seed`. In voice mode nobody has to talk: each sentence is
synthesized by Piper and handed to whisper as if it had been recorded, so
the microphone stream, the transcription and the full reply path run for
real. Leave the window alone while it runs (about three minutes).

Per turn it prints the camera frames reaching the window per second, the
idle callbacks per second (Tk repaints from the idle queue; if this drops
to zero the window has frozen even if timers still fire), whether a reply
arrived, and any main-thread stall longer than `--stall` seconds (default
0.4) with the Python stack it was stuck in. It ends with `PASS` or `FAIL`
and exits non-zero on failure. `--interval` sets the seconds between turns
(default 16).

## Layout of the package

```
main.py, __main__.py   composition root and entrypoint (Tk on the main thread)
config.py, constants.py, errors.py
conversation.py        turns and the pending intent
intents/               wake word, rules parser (one extractor per model), Gemini parser
dialogue/              orchestrator, missing-field prompts, reply tables, tone
api_client/            httpx client for the REST API
speech/                whisper speech-to-text, Piper text-to-speech
emotion/               camera, haar cascade face locator, ONNX emotion classifier
workers/               camera thread, listening and speaking coroutines
ui/                    CustomTkinter window, bridge to the asyncio thread, widgets, avatar renderer
e2e/                   end-to-end smoke test (`python -m app.e2e`), see above
```

## Adding an eleventh model

1. Add a `FieldExtractor` under `intents/rules/extractors/` and register it
   with its Spanish keywords in `intents/rules/registry.py` (the same table
   feeds Gemini's catalog).
2. Add its missing-field questions to `dialogue/missing_field_prompts.py`
   and its reply template to `dialogue/prediction_replies.py`.
3. Gemini reads the model's schema from the API at startup, nothing else to
   register.
