"""API Router v1"""
from fastapi import APIRouter
from src.pool_api.api.pool import pool_api


def get_api_router() -> APIRouter:
    """Get API router for api"""
    api_router = APIRouter(prefix="/pool")
    api_router.include_router(router=pool_api.router, prefix="")
    return api_router
