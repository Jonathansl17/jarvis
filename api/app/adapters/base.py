"""Shared contract every per-model adapter satisfies, framework-free."""

from dataclasses import dataclass
from typing import Any, ClassVar, Protocol

from pydantic import BaseModel


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
