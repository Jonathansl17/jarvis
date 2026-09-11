"""Wire contract for the telecom churn classification model."""

from typing import Literal

from pydantic import BaseModel

from app.schemas.common import PredictionMeta

_YES_NO = Literal["Yes", "No"]
_LINE_OPTION = Literal["No", "No phone service", "Yes"]
_ADDON_OPTION = Literal["No", "No internet service", "Yes"]


class TelecomChurnClassificationRequest(BaseModel):
    """A subscriber's account and service attributes."""

    gender: Literal["Male", "Female"]
    SeniorCitizen: bool
    Partner: _YES_NO
    Dependents: _YES_NO
    PhoneService: _YES_NO
    MultipleLines: _LINE_OPTION
    InternetService: Literal["DSL", "Fiber optic", "No"]
    OnlineSecurity: _ADDON_OPTION
    OnlineBackup: _ADDON_OPTION
    DeviceProtection: _ADDON_OPTION
    TechSupport: _ADDON_OPTION
    StreamingTV: _ADDON_OPTION
    StreamingMovies: _ADDON_OPTION
    Contract: Literal["Month-to-month", "One year", "Two year"]
    PaperlessBilling: _YES_NO
    PaymentMethod: Literal[
        "Bank transfer (automatic)",
        "Credit card (automatic)",
        "Electronic check",
        "Mailed check",
    ]
    tenure: float
    MonthlyCharges: float
    TotalCharges: float | None = None


class TelecomChurnClassificationResponse(BaseModel):
    """Predicted churn risk."""

    label: str
    probability: float
    threshold: float
    meta: PredictionMeta
