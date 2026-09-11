"""Composition root: builds settings, the registry, and the FastAPI app."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.adapters import ADAPTERS
from app.config import Settings, get_settings
from app.errors import register_exception_handlers
from app.registry import ModelRegistry
from app.routers import health, models, predict


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the FastAPI application, its routers, and its lifespan hook."""
    app_settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        registry = ModelRegistry(app_settings.models_dir, ADAPTERS)
        registry.load()
        app.state.registry = registry
        yield

    app = FastAPI(lifespan=lifespan)
    register_exception_handlers(app)
    app.include_router(health.router)
    app.include_router(models.router)
    app.include_router(predict.router)
    return app


app = create_app()
