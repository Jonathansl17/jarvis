"""Adapter for the avocado price regression model."""

from typing import Any, ClassVar

import pandas as pd

from app.constants import AVOCADO_REGION_COLUMN_PREFIX
from app.errors import InvalidInputError
from app.schemas.avocado_price_regression import (
    AvocadoPriceRegressionRequest,
    AvocadoPriceRegressionResponse,
)
from app.schemas.common import PredictionMeta

_VOLUME_FIELDS = {
    "Total Volume": "total_volume",
    "4046": "plu_4046",
    "4225": "plu_4225",
    "4770": "plu_4770",
    "Total Bags": "total_bags",
    "Small Bags": "small_bags",
    "Large Bags": "large_bags",
    "XLarge Bags": "xlarge_bags",
}


class AvocadoPriceRegressionAdapter:
    """Builds the region one-hot and volume columns for the forest regressor."""

    name: ClassVar[str] = "avocado_price_regression"
    request_model: ClassVar[type] = AvocadoPriceRegressionRequest
    response_model: ClassVar[type] = AvocadoPriceRegressionResponse

    def __init__(self, bundle: dict[str, Any]) -> None:
        self._model = bundle["model"]
        self._features = bundle["features"]
        self._region_columns = bundle["region_columns"]
        self._type_encoding = bundle["type_encoding"]

    def predict(
        self, request: AvocadoPriceRegressionRequest
    ) -> AvocadoPriceRegressionResponse:
        region_column = self._region_column(request.region)
        row = dict.fromkeys(self._features, 0.0)
        row.update({feature: getattr(request, field) for feature, field in _VOLUME_FIELDS.items()})
        row["year"] = float(request.date.year)
        row["month"] = float(request.date.month)
        row["week"] = float(request.date.isocalendar().week)
        row["type_organic"] = float(self._type_encoding[request.type])
        row[region_column] = 1.0
        frame = pd.DataFrame([[row[f] for f in self._features]], columns=self._features)
        predicted_price = float(self._model.predict(frame)[0])
        return AvocadoPriceRegressionResponse(
            predicted_price=predicted_price, meta=PredictionMeta(model=self.name)
        )

    def _region_column(self, region: str) -> str:
        column = f"{AVOCADO_REGION_COLUMN_PREFIX}{region}"
        if column not in self._region_columns:
            raise InvalidInputError(f"unknown region: {region!r}")
        return column
