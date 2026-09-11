"""httpx-backed `PredictionClient` implementation for the REST API in `api/`."""

from typing import Any

import httpx

from app.constants import (
    HEALTH_ROUTE,
    MODEL_SCHEMA_ROUTE_TEMPLATE,
    MODELS_ROUTE,
    OPENAPI_ROUTE,
    PREDICT_ROUTE_PREFIX,
)
from app.errors import PredictionRequestError

_REQUEST_TIMEOUT_SECONDS = 10.0


class HttpPredictionClient:
    """Talks to the prediction API over HTTP, raising on any failure."""

    def __init__(self, base_url: str) -> None:
        self._client = httpx.AsyncClient(base_url=base_url, timeout=_REQUEST_TIMEOUT_SECONDS)

    async def predict(self, model_name: str, fields: dict[str, Any]) -> dict[str, Any]:
        """Run one model's prediction and return its response body."""
        route = f"{PREDICT_ROUTE_PREFIX}/{model_name}"
        response = await self._request("POST", route, json=fields)
        return response.json()

    async def list_models(self) -> list[str]:
        """Return the names of every model the API currently serves."""
        response = await self._request("GET", MODELS_ROUTE)
        return response.json()["models"]

    async def model_schema(self, model_name: str) -> dict[str, Any]:
        """Return the JSON request schema one model expects."""
        route = MODEL_SCHEMA_ROUTE_TEMPLATE.format(model_name=model_name)
        response = await self._request("GET", route)
        return response.json()

    async def openapi_schema(self) -> dict[str, Any]:
        """Return the API's OpenAPI schema, used to prompt Gemini."""
        response = await self._request("GET", OPENAPI_ROUTE)
        return response.json()

    async def health(self) -> bool:
        """Return whether the API responds to a liveness check."""
        try:
            await self._request("GET", HEALTH_ROUTE)
        except PredictionRequestError:
            return False
        return True

    async def _request(self, method: str, route: str, **kwargs: Any) -> httpx.Response:
        """Send one HTTP request, translating transport/HTTP failures."""
        try:
            response = await self._client.request(method, route, **kwargs)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise PredictionRequestError(f"{method} {route} failed: {exc}") from exc
        return response

    async def aclose(self) -> None:
        """Release the underlying HTTP connection pool."""
        await self._client.aclose()
