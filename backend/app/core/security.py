"""Security utilities for password hashing and JWT tokens."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import cast

from app.core.config import settings
from jose import jwt
from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Validate a plain password against a hashed value."""
    return cast(bool, _pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    """Hash a password using the configured bcrypt scheme."""
    return cast(str, _pwd_context.hash(password))


def create_access_token(
    *, subject: str | int, expires_delta: timedelta | None = None
) -> str:
    """Create a signed JWT access token for the provided subject."""
    expire = datetime.now(tz=timezone.utc) + (
        expires_delta or timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    )
    to_encode = {"sub": str(subject), "exp": expire}
    return cast(
        str,
        jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGO),
    )
