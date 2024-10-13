"""API application"""
from fastapi import FastAPI

from src.pool_api.api.pool.router import get_api_router


def get_app():
    """Get FastAPI application"""
    app = FastAPI(
        title="API service",
    )
    app.include_router(router=get_api_router(), prefix="/api")
    return app
