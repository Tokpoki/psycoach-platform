"""Schemas for authentication endpoints."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, EmailStr, Field

from app.models.domain import UserRole


class RegisterRequest(BaseModel):
    """Payload required to create a new user account."""

    email: EmailStr
    password: str = Field(min_length=8)
    role: UserRole


class LoginRequest(BaseModel):
    """Credentials supplied to obtain an access token."""

    email: EmailStr
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    """JWT token returned after successful authentication."""

    access_token: str
    token_type: Literal["bearer"] = "bearer"
