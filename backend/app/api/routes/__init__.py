"""Collection of API routers exposed by the application."""

from fastapi import APIRouter

from . import auth, minigames, progress, scenarios

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(scenarios.router)
api_router.include_router(minigames.router)
api_router.include_router(progress.router)

__all__ = ["api_router"]
