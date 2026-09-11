"""Adapter for the cirrhosis binary-then-stage classification cascade."""

from typing import Any, ClassVar

import pandas as pd

from app.constants import CIRRHOSIS_SEX_POSITIVE, CIRRHOSIS_SIGN_POSITIVE
from app.schemas.cirrhosis_type_classification import (
    CirrhosisTypeClassificationRequest,
    CirrhosisTypeClassificationResponse,
)
from app.schemas.common import PredictionMeta

_SIGN_FIELDS = ("ascites", "hepatomegaly", "spiders")
_SIGN_COLUMN_NAMES = {
    "ascites": "Ascites",
    "hepatomegaly": "Hepatomegaly",
    "spiders": "Spiders",
}
_DRUG_COLUMNS = {"D-penicillamine": "Drug_penicillamine", "Placebo": "Drug_placebo"}
_CIRRHOSIS_CLASS_KEY = 1


class CirrhosisTypeClassificationAdapter:
    """Runs the binary cirrhosis model, then the stage model when positive."""

    name: ClassVar[str] = "cirrhosis_type_classification"
    request_model: ClassVar[type] = CirrhosisTypeClassificationRequest
    response_model: ClassVar[type] = CirrhosisTypeClassificationResponse

    def __init__(self, bundle: dict[str, Any]) -> None:
        self._model = bundle["model"]
        self._stage_model = bundle["stage_model"]
        self._features = bundle["features"]
        self._classes = bundle["classes"]["model"]
        self._fill_values = bundle["fill_values"]
        self._edema_encoding = bundle["encoding"]["Edema"]

    def predict(
        self, request: CirrhosisTypeClassificationRequest
    ) -> CirrhosisTypeClassificationResponse:
        frame = self._encode(request)
        predicted_class = int(self._model.predict(frame)[0])
        label = self._classes[predicted_class]
        stage = None
        if predicted_class == _CIRRHOSIS_CLASS_KEY:
            stage = int(self._stage_model.predict(frame)[0])
        return CirrhosisTypeClassificationResponse(
            label=label, stage=stage, meta=PredictionMeta(model=self.name)
        )

    def _encode(self, request: CirrhosisTypeClassificationRequest) -> pd.DataFrame:
        row = dict.fromkeys(self._features, 0.0)
        row["Age"] = request.age
        row["Sex"] = float(request.sex == CIRRHOSIS_SEX_POSITIVE)
        row["Edema"] = float(self._edema_encoding[request.edema])
        self._fill_labs(row, request)
        self._encode_signs(row, request)
        self._encode_drug(row, request)
        return pd.DataFrame([[row[f] for f in self._features]], columns=self._features)

    def _fill_labs(self, row: dict[str, float], request: CirrhosisTypeClassificationRequest) -> None:
        for field, value in self._fill_values.items():
            if field == "Age":
                continue
            requested = getattr(request, field.lower(), None)
            row[field] = value if requested is None else requested

    def _encode_signs(self, row: dict[str, float], request: CirrhosisTypeClassificationRequest) -> None:
        for field in _SIGN_FIELDS:
            column = _SIGN_COLUMN_NAMES[field]
            value = getattr(request, field)
            row[f"{column}_yes"] = float(value == CIRRHOSIS_SIGN_POSITIVE)
            row[f"{column}_unknown"] = float(value is None)

    def _encode_drug(self, row: dict[str, float], request: CirrhosisTypeClassificationRequest) -> None:
        column = _DRUG_COLUMNS.get(request.drug)
        if column:
            row[column] = 1.0
