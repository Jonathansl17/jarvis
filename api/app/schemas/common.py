"""Response envelope pieces shared by every per-model schema."""

from pydantic import BaseModel


class Warning(BaseModel):
    """One notice attached to a prediction, e.g. an out-of-range input."""

    field: str
    message: str


class PredictionMeta(BaseModel):
    """Metadata attached to every prediction response."""

    model: str
    warnings: list[Warning] = []
