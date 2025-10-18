"""Reusable dependencies for API routes."""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.domain import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Resolve the currently authenticated user from a JWT token."""
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGO])
    except JWTError as exc:  # pragma: no cover - defensive branch
        raise unauthorized from exc

    subject = payload.get("sub")
    if subject is None:
        raise unauthorized

    try:
        user_id = int(subject)
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive branch
        raise unauthorized from exc

    user = db.get(User, user_id)
    if user is None:
        raise unauthorized
    return user


def require_roles(*roles: UserRole) -> Callable[..., Awaitable[User]]:
    """Create a dependency that ensures the user has one of the specified roles."""

    async def dependency(user: User = Depends(get_current_user)) -> User:
        if roles and user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this resource.",
            )
        return user

    return dependency
