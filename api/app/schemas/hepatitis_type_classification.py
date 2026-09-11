"""Wire contract for the hepatitis type classification model."""

from typing import Literal

from pydantic import BaseModel

from app.schemas.common import PredictionMeta


class HepatitisTypeClassificationRequest(BaseModel):
    """A person's age, sex, and blood panel results."""

    age: float
    sex: Literal["m", "f"]
    ALB: float | None = None
    ALP: float | None = None
    ALT: float | None = None
    AST: float | None = None
    BIL: float | None = None
    CHE: float | None = None
    CHOL: float | None = None
    CREA: float | None = None
    GGT: float | None = None
    PROT: float | None = None


class HepatitisTypeClassificationResponse(BaseModel):
    """Predicted hepatitis category and its confidence."""

    label: str
    probability: float
    meta: PredictionMeta
