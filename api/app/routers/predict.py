"""POST /predict/{model_name} — dispatches to the matching model adapter."""

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ValidationError

from app.adapters.base import ModelAdapter
from app.constants import PREDICT_ROUTE_PREFIX
from app.errors import InvalidInputError
from app.registry import ModelRegistry, get_registry

router = APIRouter()


@router.post(f"{PREDICT_ROUTE_PREFIX}/{{model_name}}")
async def predict(
    model_name: str,
    payload: dict[str, Any],
    registry: ModelRegistry = Depends(get_registry),
) -> dict[str, Any]:
    adapter = registry.get(model_name)
    request = _validate(adapter, payload)
    response = adapter.predict(request)
    return response.model_dump()


def _validate(adapter: ModelAdapter, payload: dict[str, Any]) -> BaseModel:
    try:
        return adapter.request_model.model_validate(payload)
    except ValidationError as exc:
        raise InvalidInputError(str(exc)) from exc
