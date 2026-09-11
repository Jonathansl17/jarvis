"""Adapter for the body fat regression model."""

from typing import Any, ClassVar

import pandas as pd

from app.adapters.base import RangeWarning, check_ranges
from app.schemas.body_fat_regression import (
    BodyFatRegressionRequest,
    BodyFatRegressionResponse,
)
from app.schemas.common import PredictionMeta, Warning

_CONSTANT_COLUMN = "const"


class BodyFatRegressionAdapter:
    """Feeds abdomen/weight/wrist through the OLS model with a constant term."""

    name: ClassVar[str] = "body_fat_regression"
    request_model: ClassVar[type] = BodyFatRegressionRequest
    response_model: ClassVar[type] = BodyFatRegressionResponse

    def __init__(self, bundle: dict[str, Any]) -> None:
        self._model = bundle["model"]
        self._features = bundle["features"]
        self._training_range = bundle["training_range"]

    def predict(self, request: BodyFatRegressionRequest) -> BodyFatRegressionResponse:
        raw = {
            "Abdomen": request.abdomen,
            "Weight": request.weight,
            "Wrist": request.wrist,
        }
        row = {_CONSTANT_COLUMN: 1.0, **{f: raw[f] for f in self._features}}
        predicted_body_fat = float(self._model.predict(pd.DataFrame([row]))[0])
        warnings = check_ranges(raw, self._training_range)
        return BodyFatRegressionResponse(
            predicted_body_fat=predicted_body_fat,
            meta=PredictionMeta(model=self.name, warnings=[self._to_warning(w) for w in warnings]),
        )

    @staticmethod
    def _to_warning(warning: RangeWarning) -> Warning:
        message = f"{warning.value} is outside the training range [{warning.low}, {warning.high}]"
        return Warning(field=warning.field, message=message)
