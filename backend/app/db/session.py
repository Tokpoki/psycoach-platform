from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


if settings.DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = str(settings.DATABASE_URL)
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine_options: dict[str, object] = {"pool_pre_ping": True}

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_options["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_options)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
