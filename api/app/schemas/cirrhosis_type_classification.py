"""Wire contract for the cirrhosis type classification model."""

from typing import Literal

from pydantic import BaseModel

from app.schemas.common import PredictionMeta


class CirrhosisTypeClassificationRequest(BaseModel):
    """A patient's demographics, signs, treatment arm, and labs."""

    age: float
    sex: Literal["M", "F"]
    edema: Literal["N", "S", "Y"]
    ascites: Literal["Y", "N"] | None = None
    hepatomegaly: Literal["Y", "N"] | None = None
    spiders: Literal["Y", "N"] | None = None
    drug: Literal["D-penicillamine", "Placebo"] | None = None
    bilirubin: float | None = None
    cholesterol: float | None = None
    albumin: float | None = None
    copper: float | None = None
    alk_phos: float | None = None
    sgot: float | None = None
    tryglicerides: float | None = None
    platelets: float | None = None
    prothrombin: float | None = None


class CirrhosisTypeClassificationResponse(BaseModel):
    """Predicted binary result, plus the stage when cirrhosis is predicted."""

    label: str
    stage: int | None
    meta: PredictionMeta
