"""Wire contract for the body fat regression model."""

from pydantic import BaseModel

from app.schemas.common import PredictionMeta


class BodyFatRegressionRequest(BaseModel):
    """The three body measurements the model was trained on."""

    abdomen: float
    weight: float
    wrist: float


class BodyFatRegressionResponse(BaseModel):
    """Predicted body fat percentage."""

    predicted_body_fat: float
    meta: PredictionMeta
