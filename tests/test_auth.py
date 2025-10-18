"""Integration tests for authentication endpoints."""

from __future__ import annotations

from app.core.security import get_password_hash
from app.models.domain import UserRole
from fastapi import status

from tests.factories import UserFactory


def test_register_and_login_success(client) -> None:
    payload = {
        "email": "newuser@example.com",
        "password": "strongpass",
        "role": UserRole.ATHLETE.value,
    }

    register_response = client.post("/auth/register", json=payload)
    assert register_response.status_code == status.HTTP_201_CREATED
    response_body = register_response.json()
    assert response_body["email"] == payload["email"]
    assert response_body["role"] == payload["role"]
    assert "id" in response_body

    login_payload = {
        "email": payload["email"],
        "password": payload["password"],
    }
    login_response = client.post("/auth/login", json=login_payload)
    assert login_response.status_code == status.HTTP_200_OK
    login_body = login_response.json()
    assert login_body["token_type"] == "bearer"
    assert login_body["access_token"]


def test_login_with_wrong_password_returns_401(client, db_session) -> None:
    user = UserFactory(password_hash=get_password_hash("correct-password"))

    response = client.post(
        "/auth/login",
        json={"email": user.email, "password": "wrong-password"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect e-mail or password."


def test_register_duplicate_email_returns_400(client) -> None:
    payload = {
        "email": "duplicate@example.com",
        "password": "password123",
        "role": UserRole.ATHLETE.value,
    }
    first_response = client.post("/auth/register", json=payload)
    assert first_response.status_code == status.HTTP_201_CREATED

    second_response = client.post("/auth/register", json=payload)
    assert second_response.status_code == status.HTTP_400_BAD_REQUEST
    assert second_response.json()["detail"] == "A user with this e-mail already exists."


def test_login_unknown_user_returns_401(client) -> None:
    response = client.post(
        "/auth/login",
        json={"email": "missing@example.com", "password": "password123"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect e-mail or password."
