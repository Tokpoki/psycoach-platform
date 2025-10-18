"""Pytest fixtures for API integration tests."""

from __future__ import annotations

import sys
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure the ``app`` package is importable when running tests from the repo root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_PATH = PROJECT_ROOT / "backend"
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

from app.db.base import Base  # noqa: E402  (import after sys.path adjustment)
from app.db.session import get_db  # noqa: E402
from app.main import app  # noqa: E402

from .factories import BaseFactory  # noqa: E402


@pytest.fixture()
def session_factory() -> Generator[sessionmaker[Session], None, None]:
    """Create a fresh in-memory database for every test function."""
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    try:
        yield SessionLocal
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture()
def db_session(
    session_factory: sessionmaker[Session],
) -> Generator[Session, None, None]:
    """Provide a database session bound to the test engine."""
    session = session_factory()
    BaseFactory._meta.sqlalchemy_session = session
    for factory_cls in BaseFactory.__subclasses__():
        factory_cls._meta.sqlalchemy_session = session
    try:
        yield session
    finally:
        session.close()
        BaseFactory._meta.sqlalchemy_session = None
        for factory_cls in BaseFactory.__subclasses__():
            factory_cls._meta.sqlalchemy_session = None


@pytest.fixture()
def client(session_factory: sessionmaker[Session]) -> Generator[TestClient, None, None]:
    """Return a FastAPI test client bound to the test database session."""

    def override_get_db() -> Generator[Session, None, None]:
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.pop(get_db, None)
