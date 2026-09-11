"""Wire contract for the wine quality classification model."""

from typing import Literal

from pydantic import BaseModel

from app.schemas.common import PredictionMeta


class WineQualityClassificationRequest(BaseModel):
    """A wine's colour and laboratory measurements."""

    type: Literal["red", "white"]
    fixed_acidity: float | None = None
    volatile_acidity: float | None = None
    citric_acid: float | None = None
    residual_sugar: float | None = None
    chlorides: float | None = None
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float | None = None
    sulphates: float | None = None
    alcohol: float


class WineQualityClassificationResponse(BaseModel):
    """Predicted quality group and its confidence."""

    label: str
    probability: float
    meta: PredictionMeta
