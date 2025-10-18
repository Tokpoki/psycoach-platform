"""Authentication and authorization endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models.domain import User
from app.schemas import auth as auth_schema
from app.schemas.domain import UserPublic

router = APIRouter(tags=["auth"])


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description=(
        "Create a user account with the provided e-mail, password and role."
        " The password is stored securely using bcrypt hashing."
    ),
)
def register_user(
    payload: auth_schema.RegisterRequest, db: Session = Depends(get_db)
) -> UserPublic:
    """Register a user if the e-mail is not already taken."""
    existing_user = db.execute(
        select(User).where(User.email == payload.email)
    ).scalar_one_or_none()
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this e-mail already exists.",
        )

    user = User(
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserPublic.model_validate(user)


@router.post(
    "/login",
    response_model=auth_schema.TokenResponse,
    summary="Authenticate a user",
    description=(
        "Verify the provided credentials and return a JWT access token."
        " The token must be supplied in the Authorization header as a"
        " Bearer token for protected endpoints."
    ),
)
def login_user(
    payload: auth_schema.LoginRequest, db: Session = Depends(get_db)
) -> auth_schema.TokenResponse:
    """Validate user credentials and return a JWT access token."""
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect e-mail or password.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if user is None:
        raise invalid_credentials
    if not verify_password(payload.password, user.password_hash):
        raise invalid_credentials

    token = create_access_token(subject=str(user.id))
    return auth_schema.TokenResponse(access_token=token, token_type="bearer")
