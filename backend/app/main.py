from app.api import api_router
from app.core.config import settings
from app.core.database import ensure_database_ready
from app.core.logging import configure_logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

configure_logging()

app = FastAPI(title=settings.PROJECT_NAME)


@app.on_event("startup")
def _startup_checks() -> None:
    ensure_database_ready()

if settings.CORS_ORIGINS:
    origins = [str(origin) for origin in settings.CORS_ORIGINS]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)


@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"message": "pong"}


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> dict[str, str]:
    return {"status": "ready"}
