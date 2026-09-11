"""Wire contract for the car price regression model."""

from typing import Literal

from pydantic import BaseModel

from app.schemas.common import PredictionMeta


class CarPriceRegressionRequest(BaseModel):
    """Raw attributes of a used car, as a person would describe it."""

    present_price: float
    year: int
    kms_driven: float
    owner: int
    fuel_type: Literal["Petrol", "Diesel", "CNG"]
    seller_type: Literal["Dealer", "Individual"]
    transmission: Literal["Manual", "Automatic"]


class CarPriceRegressionResponse(BaseModel):
    """Predicted selling price, in lakhs of rupees."""

    predicted_price: float
    meta: PredictionMeta
