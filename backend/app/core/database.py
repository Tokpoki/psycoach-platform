from __future__ import annotations

import logging
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import OperationalError, ProgrammingError

from app.core.config import settings
from app.db.session import SQLALCHEMY_DATABASE_URL, engine

logger = logging.getLogger(__name__)

_MISSING_TABLE_MARKERS = (
    "does not exist",
    "no such table",
    "unknown database",
    "base table or view not found",
)


def _is_schema_error(exc: Exception) -> bool:
    """Heuristic to decide if an exception is likely caused by a missing schema."""
    message = str(exc).lower()
    return any(marker in message for marker in _MISSING_TABLE_MARKERS)


def _alembic_config() -> Config:
    config = Config()
    migrations_path = str(Path(__file__).resolve().parents[1] / "db" / "migrations")
    config.set_main_option("script_location", migrations_path)
    config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
    return config


def _upgrade_database() -> None:
    """Run Alembic migrations up to the latest revision."""
    command.upgrade(_alembic_config(), "head")


def _verify_backend_type() -> None:
    """Ensure the configured database backend matches expectations."""
    expected_backend = "postgresql" if settings.DATABASE_URL else "sqlite"
    actual_backend = engine.url.get_backend_name()
    if expected_backend != actual_backend:
        logger.warning(
            "Configured database backend (%s) does not match detected backend (%s). "
            "Continuing, but migrations will be applied to align the schema.",
            expected_backend,
            actual_backend,
        )


def ensure_database_ready() -> None:
    """Verify that the database schema exists, running migrations if necessary."""
    _verify_backend_type()

    try:
        with engine.begin() as connection:  # type: Connection
            # Probe a representative table to confirm schema availability.
            connection.execute(text("SELECT 1 FROM users LIMIT 1"))
    except (ProgrammingError, OperationalError) as exc:
        if _is_schema_error(exc):
            logger.warning(
                "Database schema appears to be missing or incompatible (%s). "
                "Attempting to apply migrations automatically.",
                exc,
            )
            _upgrade_database()
            with engine.begin() as connection:  # type: Connection
                connection.execute(text("SELECT 1 FROM users LIMIT 1"))
        else:
            raise
