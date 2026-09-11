"""GET /models — lists the names of every loaded model."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.constants import MODELS_ROUTE
from app.registry import ModelRegistry, get_registry

router = APIRouter()


class ModelsResponse(BaseModel):
    """The names of every model currently served."""

    models: list[str]


@router.get(MODELS_ROUTE, response_model=ModelsResponse)
async def list_models(registry: ModelRegistry = Depends(get_registry)) -> ModelsResponse:
    return ModelsResponse(models=registry.names())
