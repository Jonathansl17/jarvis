"""Adapter for the hepatitis type classification model."""

from typing import Any, ClassVar

import pandas as pd

from app.constants import HEPATITIS_SEX_POSITIVE
from app.schemas.common import PredictionMeta
from app.schemas.hepatitis_type_classification import (
    HepatitisTypeClassificationRequest,
    HepatitisTypeClassificationResponse,
)

_NON_LAB_FEATURES = {"Age", "Sex"}


class HepatitisTypeClassificationAdapter:
    """Fills missing labs and reports the Naive Bayes predicted category."""

    name: ClassVar[str] = "hepatitis_type_classification"
    request_model: ClassVar[type] = HepatitisTypeClassificationRequest
    response_model: ClassVar[type] = HepatitisTypeClassificationResponse

    def __init__(self, bundle: dict[str, Any]) -> None:
        self._model = bundle["model"]
        self._features = bundle["features"]
        self._fill_values = bundle["fill_values"]

    def predict(
        self, request: HepatitisTypeClassificationRequest
    ) -> HepatitisTypeClassificationResponse:
        row = self._encode(request)
        frame = pd.DataFrame([[row[f] for f in self._features]], columns=self._features)
        label = str(self._model.predict(frame)[0])
        classes = list(self._model.classes_)
        probability = float(self._model.predict_proba(frame)[0, classes.index(label)])
        return HepatitisTypeClassificationResponse(
            label=label,
            probability=probability,
            meta=PredictionMeta(model=self.name),
        )

    def _encode(self, request: HepatitisTypeClassificationRequest) -> dict[str, float]:
        row: dict[str, float] = {
            "Age": request.age,
            "Sex": float(request.sex == HEPATITIS_SEX_POSITIVE),
        }
        payload = request.model_dump()
        for feature in self._features:
            if feature in _NON_LAB_FEATURES:
                continue
            value = payload.get(feature)
            row[feature] = self._fill_values[feature] if value is None else value
        return row
