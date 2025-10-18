"""Tests for mini-game result submissions."""

from __future__ import annotations

from app.core.security import create_access_token
from app.models.domain import MiniGameType
from fastapi import status

from tests.factories import MiniGameResultFactory, ProgressFactory, UserFactory


def test_submit_mini_game_result_creates_progress_entry(client, db_session) -> None:
    user = UserFactory()
    token = create_access_token(subject=user.id)

    response = client.post(
        f"/minigames/{MiniGameType.FOCUS.value}/result",
        headers={"Authorization": f"Bearer {token}"},
        json={"score": 90},
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["result"]["score"] == 90
    assert body["progress"]["points"] == 90
    assert body["progress"]["level"] == 1
    assert body["progress"]["badges"] == []


def test_submit_mini_game_result_awards_mastery_badge(client, db_session) -> None:
    progress = ProgressFactory(points=320, level=4, badges=[])
    user = progress.user
    MiniGameResultFactory(user=user, score=240)

    token = create_access_token(subject=user.id)
    starting_points = progress.points
    response = client.post(
        f"/minigames/{MiniGameType.FOCUS.value}/result",
        headers={"Authorization": f"Bearer {token}"},
        json={"score": 100},
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["result"]["score"] == 100
    assert "Мастер концентрации" in body["progress"]["badges"]
    assert body["progress"]["points"] == starting_points + 100
