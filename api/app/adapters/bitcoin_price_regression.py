"""Adapter for the bitcoin price forecasting model."""

from typing import Any, ClassVar

import numpy as np

from app.schemas.bitcoin_price_regression import (
    BitcoinPriceRegressionRequest,
    BitcoinPriceRegressionResponse,
    ForecastPoint,
)
from app.schemas.common import PredictionMeta

_LOWER_BOUND_COLUMN = 0
_UPPER_BOUND_COLUMN = 1
_DATE_FORMAT = "%Y-%m-%d"


class BitcoinPriceRegressionAdapter:
    """Rolls the ARIMA result forward and exponentiates the log-scale forecast."""

    name: ClassVar[str] = "bitcoin_price_regression"
    request_model: ClassVar[type] = BitcoinPriceRegressionRequest
    response_model: ClassVar[type] = BitcoinPriceRegressionResponse

    def __init__(self, bundle: dict[str, Any]) -> None:
        self._model = bundle["model"]

    def predict(
        self, request: BitcoinPriceRegressionRequest
    ) -> BitcoinPriceRegressionResponse:
        forecast = self._model.get_forecast(steps=request.days)
        predicted = np.exp(forecast.predicted_mean)
        interval = np.exp(forecast.conf_int())
        points = [
            ForecastPoint(
                date=timestamp.strftime(_DATE_FORMAT),
                price=float(predicted.loc[timestamp]),
                lower=float(interval.iloc[position, _LOWER_BOUND_COLUMN]),
                upper=float(interval.iloc[position, _UPPER_BOUND_COLUMN]),
            )
            for position, timestamp in enumerate(predicted.index)
        ]
        return BitcoinPriceRegressionResponse(
            forecast=points, meta=PredictionMeta(model=self.name)
        )
