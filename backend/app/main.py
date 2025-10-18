from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"message": "pong"}


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> dict[str, str]:
    return {"status": "ready"}
