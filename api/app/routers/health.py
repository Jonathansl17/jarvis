"""GET /health — process liveness only, no model lookup."""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from app.constants import HEALTH_ROUTE

router = APIRouter()


class HealthResponse(BaseModel):
    """The process is up and able to serve requests."""

    status: Literal["ok"]


@router.get(HEALTH_ROUTE, response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")
