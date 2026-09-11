"""Wire contract for the bitcoin price forecasting model."""

from pydantic import BaseModel, Field

from app.schemas.common import PredictionMeta

_MIN_FORECAST_DAYS = 1
_MAX_FORECAST_DAYS = 30


class BitcoinPriceRegressionRequest(BaseModel):
    """How many days ahead to forecast the closing price."""

    days: int = Field(ge=_MIN_FORECAST_DAYS, le=_MAX_FORECAST_DAYS)


class ForecastPoint(BaseModel):
    """One day's forecast, with its confidence interval."""

    date: str
    price: float
    lower: float
    upper: float


class BitcoinPriceRegressionResponse(BaseModel):
    """The requested forecast horizon."""

    forecast: list[ForecastPoint]
    meta: PredictionMeta
