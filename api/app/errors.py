"""Domain error types raised across the service and their HTTP mapping."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

_HTTP_NOT_FOUND = 404
_HTTP_UNPROCESSABLE_ENTITY = 422
_HTTP_INTERNAL_SERVER_ERROR = 500


class ApiError(Exception):
    """Base class for every domain error the service can raise."""

    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class ModelNotFoundError(ApiError):
    """Raised when a requested model name is not in the registry."""

    def __init__(self, detail: str) -> None:
        super().__init__(_HTTP_NOT_FOUND, detail)


class InvalidInputError(ApiError):
    """Raised when a request body fails validation for a model."""

    def __init__(self, detail: str) -> None:
        super().__init__(_HTTP_UNPROCESSABLE_ENTITY, detail)


class PredictionError(ApiError):
    """Raised when loading a bundle or running a prediction fails."""

    def __init__(self, detail: str) -> None:
        super().__init__(_HTTP_INTERNAL_SERVER_ERROR, detail)


def register_exception_handlers(app: FastAPI) -> None:
    """Install the single handler that turns any `ApiError` into JSON."""

    @app.exception_handler(ApiError)
    async def _handle_api_error(_request: Request, exc: ApiError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
