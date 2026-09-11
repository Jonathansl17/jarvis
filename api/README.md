# API

FastAPI service that serves the ten trained models under `models/*.joblib`.

## Run

From the repository root, using the project's plain venv (no lockfile tool
is used anywhere in this repo):

```bash
./env/bin/pip install -r api/requirements.txt
cd api
../env/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /health` — process liveness, no model lookup.
- `GET /models` — the names of every model currently loaded.
- `POST /predict/{model_name}` — runs one model; the request body shape is
  specific to `model_name` (see `app/schemas/<model_name>.py`).

## Configuration

Read once at startup by `app/config.py` (`pydantic-settings`), from
environment variables matched case-insensitively to these field names:

- `MODELS_DIR` — directory holding the `.joblib` bundles. Defaults to the
  repository's root `models/` directory, resolved relative to this package.
- `HOST` — bind address. Defaults to `0.0.0.0`.
- `PORT` — bind port. Defaults to `8000`.

## Adding an eleventh model

1. Train it and dump a bundle dict to `models/<model_name>.joblib`, carrying
   every value the adapter will need (features, fill values, thresholds,
   encodings, classes, training ranges) — never hardcode these in the API.
2. Add `app/schemas/<model_name>.py` declaring `<Name>Request` /
   `<Name>Response`.
3. Add `app/adapters/<model_name>.py` implementing the `ModelAdapter`
   contract from `app/adapters/base.py` against that schema.
4. Register the new adapter class in `app/adapters/__init__.py`'s `ADAPTERS`
   mapping — this is the only Open/Closed seam; no router or registry code
   changes.
