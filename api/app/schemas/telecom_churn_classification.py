"""Wire contract for the telecom churn classification model."""

from typing import Literal, Self

from pydantic import BaseModel, model_validator

from app.schemas.common import PredictionMeta

_YES_NO = Literal["Yes", "No"]
_LINE_OPTION = Literal["No", "No phone service", "Yes"]
_ADDON_OPTION = Literal["No", "No internet service", "Yes"]
_NO_INTERNET = "No"
_NO_INTERNET_SERVICE = "No internet service"
_NO_PHONE = "No"
_NO_PHONE_SERVICE = "No phone service"
_INTERNET_ADDONS = (
    "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"
)


class TelecomChurnClassificationRequest(BaseModel):
    """A subscriber's account and service attributes.

    The internet add-ons may be omitted when the subscriber has no internet,
    and the multiple-lines flag when there is no phone service: the dataset
    codes those cases as their own category, filled in here.
    """

    gender: Literal["Male", "Female"]
    SeniorCitizen: bool
    Partner: _YES_NO
    Dependents: _YES_NO
    PhoneService: _YES_NO
    MultipleLines: _LINE_OPTION | None = None
    InternetService: Literal["DSL", "Fiber optic", "No"]
    OnlineSecurity: _ADDON_OPTION | None = None
    OnlineBackup: _ADDON_OPTION | None = None
    DeviceProtection: _ADDON_OPTION | None = None
    TechSupport: _ADDON_OPTION | None = None
    StreamingTV: _ADDON_OPTION | None = None
    StreamingMovies: _ADDON_OPTION | None = None
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

    @model_validator(mode="after")
    def fill_service_dependent_fields(self) -> Self:
        """Derive the add-on codes from the absence of internet or phone service."""
        if self.InternetService == _NO_INTERNET:
            for name in _INTERNET_ADDONS:
                if getattr(self, name) is None:
                    setattr(self, name, _NO_INTERNET_SERVICE)
        if self.PhoneService == _NO_PHONE and self.MultipleLines is None:
            self.MultipleLines = _NO_PHONE_SERVICE
        missing = [name for name in (*_INTERNET_ADDONS, "MultipleLines") if getattr(self, name) is None]
        if missing:
            raise ValueError(f"required when the service exists: {', '.join(missing)}")
        return self


class TelecomChurnClassificationResponse(BaseModel):
    """Predicted churn risk."""

    label: str
    probability: float
    threshold: float
    meta: PredictionMeta
