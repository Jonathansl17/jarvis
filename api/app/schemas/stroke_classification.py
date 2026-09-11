"""Wire contract for the stroke classification model."""

from typing import Literal

from pydantic import BaseModel

from app.schemas.common import PredictionMeta


class StrokeClassificationRequest(BaseModel):
    """A person's medical and lifestyle facts."""

    gender: Literal["Male", "Female"]
    age: float
    hypertension: bool
    heart_disease: bool
    ever_married: Literal["Yes", "No"]
    work_type: Literal[
        "Govt_job", "Private", "Self-employed", "children", "Never_worked"
    ]
    Residence_type: Literal["Urban", "Rural"]
    avg_glucose_level: float
    bmi: float | None = None
    smoking_status: Literal[
        "formerly smoked", "never smoked", "smokes", "Unknown"
    ]


class StrokeClassificationResponse(BaseModel):
    """Predicted stroke risk."""

    label: str
    probability: float
    threshold: float
    meta: PredictionMeta
