"""Adapter for the flight delay regression model."""

from typing import Any, ClassVar

import pandas as pd

from app.errors import InvalidInputError
from app.schemas.common import PredictionMeta
from app.schemas.flight_delay_regression import (
    FlightDelayRegressionRequest,
    FlightDelayRegressionResponse,
)


class FlightDelayRegressionAdapter:
    """Maps carrier/airport codes through their frequency maps and predicts."""

    name: ClassVar[str] = "flight_delay_regression"
    request_model: ClassVar[type] = FlightDelayRegressionRequest
    response_model: ClassVar[type] = FlightDelayRegressionResponse

    def __init__(self, bundle: dict[str, Any]) -> None:
        self._model = bundle["model"]
        self._features = bundle["features"]
        self._carrier_encoding = bundle["carrier_encoding"]
        self._airport_encoding = bundle["airport_encoding"]
        self._dest_encoding = bundle["dest_encoding"]

    def predict(
        self, request: FlightDelayRegressionRequest
    ) -> FlightDelayRegressionResponse:
        row = {
            "Month": request.month,
            "DayOfWeek": request.day_of_week,
            "DayofMonth": request.day_of_month,
            "DepHour": request.dep_hour,
            "Carrier_code": self._lookup(self._carrier_encoding, request.carrier, "carrier"),
            "Distance": request.distance,
            "Origin_freq": self._lookup(self._airport_encoding, request.origin, "origin airport"),
            "Dest_freq": self._lookup(self._dest_encoding, request.dest, "destination airport"),
        }
        frame = pd.DataFrame([[row[f] for f in self._features]], columns=self._features)
        predicted_delay_minutes = float(self._model.predict(frame)[0])
        return FlightDelayRegressionResponse(
            predicted_delay_minutes=predicted_delay_minutes,
            meta=PredictionMeta(model=self.name),
        )

    @staticmethod
    def _lookup(encoding: dict[str, float], code: str, label: str) -> float:
        if code not in encoding:
            raise InvalidInputError(f"unknown {label} code: {code!r}")
        return float(encoding[code])
