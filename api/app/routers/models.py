"""GET /models and GET /models/{model_name}/schema."""

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.constants import MODEL_SCHEMA_ROUTE, MODELS_ROUTE
from app.registry import ModelRegistry, get_registry

router = APIRouter()


class ModelsResponse(BaseModel):
    """The names of every model currently served."""

    models: list[str]


@router.get(MODELS_ROUTE, response_model=ModelsResponse)
async def list_models(registry: ModelRegistry = Depends(get_registry)) -> ModelsResponse:
    return ModelsResponse(models=registry.names())


@router.get(MODEL_SCHEMA_ROUTE)
async def model_schema(
    model_name: str, registry: ModelRegistry = Depends(get_registry)
) -> dict[str, Any]:
    """JSON schema of the request body one model expects, for clients that build inputs dynamically."""
    return registry.get(model_name).request_model.model_json_schema()
