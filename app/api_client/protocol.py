"""The contract for talking to the REST API in `api/`."""

from typing import Any, Protocol


class PredictionClient(Protocol):
    """Calls the prediction API and reports its shape and liveness."""

    async def predict(self, model_name: str, fields: dict[str, Any]) -> dict[str, Any]: ...

    async def list_models(self) -> list[str]: ...

    async def openapi_schema(self) -> dict[str, Any]: ...

    async def health(self) -> bool: ...
