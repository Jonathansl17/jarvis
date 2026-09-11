"""Shared contract every per-model adapter satisfies, framework-free."""

from dataclasses import dataclass
from typing import Any, ClassVar, Protocol

import pandas as pd
from pydantic import BaseModel

from app.schemas.common import Warning


class ModelAdapter(Protocol):
    """Translates a human-facing request into a prediction and back."""

    name: ClassVar[str]
    request_model: ClassVar[type[BaseModel]]
    response_model: ClassVar[type[BaseModel]]

    def __init__(self, bundle: dict[str, Any]) -> None: ...

    def predict(self, request: BaseModel) -> BaseModel: ...


@dataclass(frozen=True)
class RangeWarning:
    """One field whose input value fell outside its training range."""

    field: str
    value: float
    low: float
    high: float


def check_ranges(
    values: dict[str, float],
    training_range: dict[str, tuple[float, float]],
) -> list[RangeWarning]:
    """Return a `RangeWarning` for every value outside its training bounds."""
    warnings: list[RangeWarning] = []
    for field, (low, high) in training_range.items():
        if field not in values:
            continue
        value = values[field]
        if value < low or value > high:
            warnings.append(RangeWarning(field=field, value=value, low=low, high=high))
    return warnings


def to_warning(warning: RangeWarning) -> Warning:
    """Render a `RangeWarning` as the wire-facing `Warning` schema."""
    message = f"{warning.value} is outside the training range [{warning.low}, {warning.high}]"
    return Warning(field=warning.field, message=message)


def frame_from_row(row: dict[str, Any], features: list[str]) -> pd.DataFrame:
    """Build the single-row prediction frame in the bundle's declared feature order."""
    return pd.DataFrame([[row[f] for f in features]], columns=features)


def label_and_probability(model: Any, frame: pd.DataFrame) -> tuple[str, float]:
    """Return the predicted label and its probability from a `classes_` estimator."""
    label = str(model.predict(frame)[0])
    classes = list(model.classes_)
    probability = float(model.predict_proba(frame)[0, classes.index(label)])
    return label, probability
