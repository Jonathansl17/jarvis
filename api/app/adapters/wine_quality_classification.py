"""Adapter for the wine quality classification model."""

from typing import Any, ClassVar

from app.adapters.base import frame_from_row, label_and_probability
from app.constants import WINE_TYPE_ENCODING
from app.schemas.common import PredictionMeta
from app.schemas.wine_quality_classification import (
    WineQualityClassificationRequest,
    WineQualityClassificationResponse,
)

_FIELD_TO_FEATURE = {
    "fixed_acidity": "fixed acidity",
    "volatile_acidity": "volatile acidity",
    "citric_acid": "citric acid",
    "residual_sugar": "residual sugar",
    "chlorides": "chlorides",
    "free_sulfur_dioxide": "free sulfur dioxide",
    "total_sulfur_dioxide": "total sulfur dioxide",
    "density": "density",
    "pH": "pH",
    "sulphates": "sulphates",
    "alcohol": "alcohol",
}


class WineQualityClassificationAdapter:
    """Fills missing measurements and reports the KNN predicted quality group."""

    name: ClassVar[str] = "wine_quality_classification"
    request_model: ClassVar[type] = WineQualityClassificationRequest
    response_model: ClassVar[type] = WineQualityClassificationResponse

    def __init__(self, bundle: dict[str, Any]) -> None:
        self._model = bundle["model"]
        self._features = bundle["features"]
        self._fill_values = bundle["fill_values"]

    def predict(
        self, request: WineQualityClassificationRequest
    ) -> WineQualityClassificationResponse:
        row = self._encode(request)
        frame = frame_from_row(row, self._features)
        label, probability = label_and_probability(self._model, frame)
        return WineQualityClassificationResponse(
            label=label, probability=probability, meta=PredictionMeta(model=self.name)
        )

    def _encode(self, request: WineQualityClassificationRequest) -> dict[str, float]:
        row: dict[str, float] = {"type": float(WINE_TYPE_ENCODING[request.type])}
        payload = request.model_dump()
        for field, feature in _FIELD_TO_FEATURE.items():
            value = payload[field]
            row[feature] = self._fill_values.get(feature, value) if value is None else value
        return row
