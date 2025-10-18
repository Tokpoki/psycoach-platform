"""Collection of API routers exposed by the application."""

from fastapi import APIRouter

from . import auth, scenarios

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(scenarios.router)

__all__ = ["api_router"]
