"""End-to-end smoke test of the desktop app: `python -m app.e2e`.

Runs the real window against the real API, whisper, Piper and webcam, one
random example sentence per model from `app/prompts.txt`, and fails if a
turn goes unanswered or the Tk main thread stalls. See `app/README.md`.
"""
