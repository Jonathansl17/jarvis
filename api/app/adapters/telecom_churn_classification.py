"""Adapter for the telecom churn classification model."""

from typing import Any, ClassVar

from app.adapters.base import frame_from_row
from app.schemas.common import PredictionMeta
from app.schemas.telecom_churn_classification import (
    TelecomChurnClassificationRequest,
    TelecomChurnClassificationResponse,
)

_CATEGORICAL_FIELDS = (
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
)
_POSITIVE_CLASS_INDEX = 1


class TelecomChurnClassificationAdapter:
    """One-hot encodes the account attributes and scores churn risk."""

    name: ClassVar[str] = "telecom_churn_classification"
    request_model: ClassVar[type] = TelecomChurnClassificationRequest
    response_model: ClassVar[type] = TelecomChurnClassificationResponse

    def __init__(self, bundle: dict[str, Any]) -> None:
        self._model = bundle["model"]
        self._features = bundle["features"]
        self._threshold = bundle["threshold"]
        self._total_charges_fill = bundle["total_charges_fill"]

    def predict(
        self, request: TelecomChurnClassificationRequest
    ) -> TelecomChurnClassificationResponse:
        row = self._encode(request)
        frame = frame_from_row(row, self._features)
        probability = float(self._model.predict_proba(frame)[0, _POSITIVE_CLASS_INDEX])
        label = "churn" if probability >= self._threshold else "no churn"
        return TelecomChurnClassificationResponse(
            label=label,
            probability=probability,
            threshold=self._threshold,
            meta=PredictionMeta(model=self.name),
        )

    def _encode(self, request: TelecomChurnClassificationRequest) -> dict[str, float]:
        total_charges = request.TotalCharges
        row = dict.fromkeys(self._features, 0.0)
        row.update(
            {
                "SeniorCitizen": float(request.SeniorCitizen),
                "tenure": request.tenure,
                "MonthlyCharges": request.MonthlyCharges,
                "TotalCharges": self._total_charges_fill if total_charges is None else total_charges,
            }
        )
        for field in _CATEGORICAL_FIELDS:
            column = f"{field}_{getattr(request, field)}"
            if column in row:
                row[column] = 1.0
        return row
