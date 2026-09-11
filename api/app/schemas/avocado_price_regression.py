"""Wire contract for the avocado price regression model."""

from datetime import date
from typing import Literal

from pydantic import BaseModel

from app.schemas.common import PredictionMeta


class AvocadoPriceRegressionRequest(BaseModel):
    """A week's sales volumes for one avocado type and region."""

    type: Literal["conventional", "organic"]
    region: str
    date: date
    total_volume: float
    plu_4046: float
    plu_4225: float
    plu_4770: float
    total_bags: float
    small_bags: float
    large_bags: float
    xlarge_bags: float


class AvocadoPriceRegressionResponse(BaseModel):
    """Predicted average price."""

    predicted_price: float
    meta: PredictionMeta
