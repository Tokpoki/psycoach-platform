"""Tests for scenario listing and choice application."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.core.security import create_access_token
from app.models.domain import ScenarioKind, UserRole
from fastapi import status
from jose import jwt

from tests.factories import ChoiceFactory, ScenarioFactory, UserFactory


def test_list_scenarios_filters_by_role_and_kind(client, db_session) -> None:
    ScenarioFactory(title="All Roles", role_scope=None, kind=ScenarioKind.PRESTART)
    ScenarioFactory(
        title="Athlete Prestart",
        role_scope=UserRole.ATHLETE,
        kind=ScenarioKind.PRESTART,
    )
    ScenarioFactory(
        title="Coach Defeat", role_scope=UserRole.COACH, kind=ScenarioKind.DEFEAT
    )

    response = client.get(
        "/scenarios",
        params={"role": UserRole.ATHLETE.value, "kind": ScenarioKind.PRESTART.value},
    )

    assert response.status_code == status.HTTP_200_OK
    titles = [item["title"] for item in response.json()]
    assert "All Roles" in titles
    assert "Athlete Prestart" in titles
    assert "Coach Defeat" not in titles


def test_apply_choice_updates_progress_and_returns_context(client, db_session) -> None:
    user = UserFactory()
    scenario = ScenarioFactory()
    choice = ChoiceFactory(scenario=scenario, score_delta=150, skill_tags=["calm"])

    token = create_access_token(subject=user.id)
    response = client.post(
        f"/scenarios/{scenario.id}/choice",
        headers={"Authorization": f"Bearer {token}"},
        json={"choice_id": choice.id},
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["new_points"] == 150
    assert body["new_level"] == 2
    assert body["applied_skill"] == ["calm"]
    assert body["new_badges"] == ["Level 2 achiever"]


def test_apply_choice_rejects_token_without_subject(client, db_session) -> None:
    scenario = ScenarioFactory()
    choice = scenario.choices[0]

    token = jwt.encode(
        {"exp": datetime.now(timezone.utc) + timedelta(minutes=5)},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGO,
    )

    response = client.post(
        f"/scenarios/{scenario.id}/choice",
        headers={"Authorization": f"Bearer {token}"},
        json={"choice_id": choice.id},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Could not validate credentials."


def test_apply_choice_rejects_unknown_user(client, db_session) -> None:
    scenario = ScenarioFactory()
    choice = scenario.choices[0]

    token = jwt.encode(
        {
            "sub": "9999",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        },
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGO,
    )

    response = client.post(
        f"/scenarios/{scenario.id}/choice",
        headers={"Authorization": f"Bearer {token}"},
        json={"choice_id": choice.id},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Could not validate credentials."


def test_create_scenario_requires_admin_role(client, db_session) -> None:
    user = UserFactory(role=UserRole.ATHLETE)
    token = create_access_token(subject=user.id)

    payload = {
        "title": "New Scenario",
        "kind": ScenarioKind.PRESTART.value,
        "content_json": {"body": "Stay calm"},
        "role_scope": UserRole.ATHLETE.value,
        "choices": [
            {
                "text": "Breathe",
                "explanation": "Breathing reduces stress",
                "skill_tags": ["breathing"],
                "score_delta": 20,
            }
        ],
    }

    response = client.post(
        "/scenarios",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "You do not have access to this resource."
