"""Adapter for the car price regression model."""

from typing import Any, ClassVar

import numpy as np
import pandas as pd

from app.adapters.base import check_ranges, to_warning
from app.schemas.car_price_regression import (
    CarPriceRegressionRequest,
    CarPriceRegressionResponse,
)
from app.schemas.common import PredictionMeta

_CONSTANT_COLUMN = "const"
_FUEL_COLUMNS = {"Diesel": "Fuel_Diesel", "CNG": "Fuel_CNG"}
_SELLER_INDIVIDUAL_COLUMN = "Seller_Individual"
_TRANSMISSION_AUTOMATIC_COLUMN = "Transmission_Automatic"


class CarPriceRegressionAdapter:
    """Encodes a car's attributes and decodes the OLS log-price output."""

    name: ClassVar[str] = "car_price_regression"
    request_model: ClassVar[type] = CarPriceRegressionRequest
    response_model: ClassVar[type] = CarPriceRegressionResponse

    def __init__(self, bundle: dict[str, Any]) -> None:
        self._model = bundle["model"]
        self._features = bundle["features"]
        self._reference_year = bundle["reference_year"]
        self._log_features = bundle["log_features"]
        self._log1p_features = bundle["log1p_features"]
        self._training_range = bundle["training_range"]

    def predict(self, request: CarPriceRegressionRequest) -> CarPriceRegressionResponse:
        raw = self._raw_values(request)
        frame = self._encode(raw, request)
        predicted_log = self._model.predict(frame)[0]
        predicted_price = float(np.exp(predicted_log))
        warnings = check_ranges(raw, self._training_range)
        return CarPriceRegressionResponse(
            predicted_price=predicted_price,
            meta=PredictionMeta(model=self.name, warnings=[to_warning(w) for w in warnings]),
        )

    def _raw_values(self, request: CarPriceRegressionRequest) -> dict[str, float]:
        return {
            "Present_Price": request.present_price,
            "Age": float(self._reference_year - request.year),
            "Kms_Driven": request.kms_driven,
            "Owner": float(request.owner),
        }

    def _encode(self, raw: dict[str, float], request: CarPriceRegressionRequest) -> pd.DataFrame:
        row = dict.fromkeys(self._features, 0.0)
        row.update(raw)
        for feature in self._log_features:
            row[feature] = float(np.log(raw[feature]))
        for feature in self._log1p_features:
            row[feature] = float(np.log1p(raw[feature]))
        fuel_column = _FUEL_COLUMNS.get(request.fuel_type)
        if fuel_column:
            row[fuel_column] = 1.0
        if request.seller_type == "Individual":
            row[_SELLER_INDIVIDUAL_COLUMN] = 1.0
        if request.transmission == "Automatic":
            row[_TRANSMISSION_AUTOMATIC_COLUMN] = 1.0
        return pd.DataFrame([{_CONSTANT_COLUMN: 1.0, **{f: row[f] for f in self._features}}])
