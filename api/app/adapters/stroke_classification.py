"""Adapter for the stroke classification model."""

from typing import Any, ClassVar

from app.adapters.base import frame_from_row
from app.constants import (
    STROKE_GENDER_POSITIVE,
    STROKE_MARRIED_POSITIVE,
    STROKE_RESIDENCE_POSITIVE,
)
from app.schemas.common import PredictionMeta
from app.schemas.stroke_classification import (
    StrokeClassificationRequest,
    StrokeClassificationResponse,
)

_WORK_TYPE_PREFIX = "work_type"
_SMOKING_STATUS_PREFIX = "smoking_status"
_POSITIVE_CLASS_INDEX = 1


class StrokeClassificationAdapter:
    """Expands human input into the Pipeline's one-hot columns and scores it."""

    name: ClassVar[str] = "stroke_classification"
    request_model: ClassVar[type] = StrokeClassificationRequest
    response_model: ClassVar[type] = StrokeClassificationResponse

    def __init__(self, bundle: dict[str, Any]) -> None:
        self._model = bundle["model"]
        self._features = bundle["features"]
        self._threshold = bundle["threshold"]
        self._bmi_fill = bundle["bmi_fill"]
        self._reference_categories = bundle["reference_categories"]

    def predict(self, request: StrokeClassificationRequest) -> StrokeClassificationResponse:
        row = self._encode(request)
        frame = frame_from_row(row, self._features)
        probability = float(self._model.predict_proba(frame)[0, _POSITIVE_CLASS_INDEX])
        label = "stroke" if probability >= self._threshold else "no stroke"
        return StrokeClassificationResponse(
            label=label,
            probability=probability,
            threshold=self._threshold,
            meta=PredictionMeta(model=self.name),
        )

    def _encode(self, request: StrokeClassificationRequest) -> dict[str, float]:
        bmi_missing = request.bmi is None
        row = dict.fromkeys(self._features, 0.0)
        row.update(
            {
                "gender": float(request.gender == STROKE_GENDER_POSITIVE),
                "age": request.age,
                "hypertension": float(request.hypertension),
                "heart_disease": float(request.heart_disease),
                "ever_married": float(request.ever_married == STROKE_MARRIED_POSITIVE),
                "Residence_type": float(request.Residence_type == STROKE_RESIDENCE_POSITIVE),
                "avg_glucose_level": request.avg_glucose_level,
                "bmi": self._bmi_fill if bmi_missing else request.bmi,
                "bmi_missing": float(bmi_missing),
            }
        )
        self._set_dummy(row, _WORK_TYPE_PREFIX, request.work_type)
        self._set_dummy(row, _SMOKING_STATUS_PREFIX, request.smoking_status)
        return row

    def _set_dummy(self, row: dict[str, float], prefix: str, value: str) -> None:
        if value == self._reference_categories[prefix]:
            return
        column = f"{prefix}_{value}"
        if column in row:
            row[column] = 1.0
