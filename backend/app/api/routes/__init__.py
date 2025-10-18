"""Collection of API routers exposed by the application."""

from fastapi import APIRouter

from . import auth

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth")

__all__ = ["api_router"]
