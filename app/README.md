# App

JarvisTEC — a Textual TUI voice assistant. Wake word → speech-to-text →
intent parsing (keyword rules, or Gemini when configured) → the REST API in
`api/` → tone-adjusted reply → text-to-speech, with a background webcam
emotion sampler feeding both the tone adapter and the avatar.

## Run

From the repository root, using the project's plain venv (no lockfile tool
is used anywhere in this repo):

```bash
./env/bin/pip install -r app/requirements.txt
cp app/.env.example app/.env   # fill in GEMINI_API_KEY (optional), API_BASE_URL
./env/bin/python -m app
```

The API in `api/` must be running and reachable at `API_BASE_URL` for
predictions and for fetching model schemas at startup.

## Configuration

Read once at startup by `app/config.py` (`pydantic-settings`), from
`app/.env` or the environment, matched case-insensitively to these field
names:

- `GEMINI_API_KEY` — optional. Without it, intents are parsed by keyword
  rules only (`intents/rules/`). With it, Gemini is tried first and the
  rules parser is the fallback on any Gemini failure.
- `GEMINI_MODELS` — comma-separated Gemini models, tried in order; a model
  whose free-tier quota is exhausted (429) or that has been retired (404)
  is skipped in favor of the next one for the rest of the session. Defaults
  to `gemini-3.6-flash,gemini-flash-lite-latest`.
- `API_BASE_URL` — base URL of the REST API in `api/`. Defaults to
  `http://localhost:8000`.
- `MODELS_DIR` — directory holding `facial_emotion_cnn.onnx` and
  `haarcascade_frontalface_alt.xml`. Defaults to the repository's root
  `models/` directory, shared read-only with `api/`.
- `PIPER_CACHE_DIR` — where the Spanish Piper voice is downloaded and
  cached. Defaults to `app/.cache/piper/`.
- `CAMERA_ENABLED` — turn the webcam emotion sampler on or off. Defaults to
  `true`. Also toggleable at runtime with the `e` key.
- `TTS_ENABLED` — turn speech synthesis on or off. Defaults to `true`.

## Interaction

- Type a message and press `Enter`, or press `Ctrl+Espacio` to start
  recording and again to stop and transcribe (`Ctrl+T` is a second binding
  for the same action, for terminals that swallow Ctrl+Space). Both paths
  end up in the same `DialogueOrchestrator.handle_user_text()` call. Space
  is always a normal character in the input line.
- `Ctrl+Q` quits. `Ctrl+E` toggles the webcam emotion sampler. `Tab` switches
  focus between the input line and the conversation log for scrollback.
- The avatar, status bar, colors, and timings follow the visual spec
  verbatim (`ui/frames.py` for frame art, `ui/styles.tcss` for tokens).
- The camera preview always shows the full webcam frame, mirrored, with the
  detected face boxed live. It grabs a preview frame every
  `PREVIEW_INTERVAL_SECONDS` but only re-runs face detection and emotion
  classification every `EMOTION_SAMPLE_INTERVAL_SECONDS`, reusing the last
  result in between so the box stays drawn without re-running the model on
  every frame. Below the preview, one line names the detected emotion in
  Spanish with its confidence (e.g. "feliz 82 %"), or "sin rostro" when the
  camera is on but no face is found.

## Adding an eleventh model

The assistant never special-cases a model by name:

1. Add a keyword-based `FieldExtractor` under `intents/rules/extractors/`
   (mirroring `api/app/adapters/base.py`'s split of contract + helpers) and
   register it, plus its trigger keywords, in `intents/rules/registry.py` —
   the only Open/Closed seam on the rules side.
2. If its prediction response introduces a genuinely new shape (today's
   three are label/probability, a single value, and a list of forecast
   points), extend `dialogue/reply_builder.py`'s shape detection; otherwise
   no change is needed there.
3. Add its missing-field questions to `dialogue/missing_field_prompts.py`'s
   table. Gemini, when configured, needs no registration at all — it reads
   every model's schema from the API at startup.

## Known simplifications

- Dark palette only; the design spec's light-mode fallback (§3) is
  intentionally not implemented, per its own guidance to ship dark-only
  rather than half-test a fallback nobody will see.
- The conversation log's "── nuevos mensajes ──" re-arm-on-scroll divider
  (§5) is not implemented; the log always auto-scrolls to the newest turn.
- Mouth-sync during speech playback uses the spec's documented fallback
  (fixed 120 ms frame cycling) since the local TTS backend does not expose
  a live amplitude callback.
