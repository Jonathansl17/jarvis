"""Loads every model bundle once and serves it by name."""

from pathlib import Path
from typing import Any

import joblib
from fastapi import Request

from app.adapters.base import ModelAdapter
from app.constants import BUNDLE_FILE_SUFFIX
from app.errors import ModelNotFoundError, PredictionError


class ModelRegistry:
    """Holds one adapter instance per model, built from its `.joblib` bundle."""

    def __init__(self, models_dir: Path, adapters: dict[str, type[ModelAdapter]]) -> None:
        self._models_dir = models_dir
        self._adapter_classes = adapters
        self._adapters: dict[str, ModelAdapter] = {}

    def load(self) -> None:
        """Load every known model's bundle from disk into an adapter instance."""
        for name, adapter_class in self._adapter_classes.items():
            bundle_path = self._models_dir / f"{name}{BUNDLE_FILE_SUFFIX}"
            self._adapters[name] = adapter_class(self._load_bundle(bundle_path))

    def get(self, name: str) -> ModelAdapter:
        """Return the adapter for `name`, or raise if it was never loaded."""
        try:
            return self._adapters[name]
        except KeyError as exc:
            raise ModelNotFoundError(f"unknown model: {name!r}") from exc

    def names(self) -> list[str]:
        """Return the names of every loaded model."""
        return list(self._adapters)

    @staticmethod
    def _load_bundle(bundle_path: Path) -> dict[str, Any]:
        try:
            return joblib.load(bundle_path)
        except (OSError, EOFError) as exc:
            raise PredictionError(f"failed to load bundle: {bundle_path}") from exc


def get_registry(request: Request) -> ModelRegistry:
    """The `Depends(...)` target routers use to reach the process registry.

    Routers depend on this function's signature, never on a constructed
    `ModelRegistry` or a module-level global.
    """
    return request.app.state.registry
