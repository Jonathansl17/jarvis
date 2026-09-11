"""Wire contract for the flight delay regression model."""

from pydantic import BaseModel, Field

from app.schemas.common import PredictionMeta


class FlightDelayRegressionRequest(BaseModel):
    """A scheduled flight's calendar slot, route, and distance."""

    month: int = Field(ge=1, le=12)
    day_of_month: int = Field(ge=1, le=31)
    day_of_week: int = Field(ge=1, le=7)
    dep_hour: int = Field(ge=0, le=23)
    carrier: str
    origin: str
    dest: str
    distance: float


class FlightDelayRegressionResponse(BaseModel):
    """Predicted arrival delay, in minutes."""

    predicted_delay_minutes: float
    meta: PredictionMeta
