"""Core gameplay logic helpers."""

from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.models.domain import Choice, Progress


def apply_effect(user_id: int, choice: Choice, *, db: Session) -> dict[str, Any]:
    """Apply the outcome of a choice to the user's progress.

    The function ensures a :class:`~app.models.domain.Progress` record exists for the
    user, updates the points with the choice ``score_delta`` and adjusts the level
    according to the accumulated points. When the level increases a simple badge is
    awarded. The updated progress state is returned alongside the contextual
    information from the choice.
    """

    progress = db.get(Progress, user_id)
    if progress is None:
        progress = Progress(user_id=user_id, points=0, level=1, badges=[])
        db.add(progress)
        db.flush()

    # Normalise badges into a mutable list for manipulation.
    existing_badges = list(progress.badges or [])

    new_points = max(0, progress.points + choice.score_delta)
    progress.points = new_points

    previous_level = progress.level or 1
    new_level = max(1, new_points // 100 + 1)
    progress.level = new_level

    new_badges: list[str] = []
    if new_level > previous_level:
        badge_name = f"Level {new_level} achiever"
        if badge_name not in existing_badges:
            existing_badges.append(badge_name)
            new_badges.append(badge_name)

    progress.badges = existing_badges

    db.commit()
    db.refresh(progress)

    return {
        "applied_skill": list(choice.skill_tags or []),
        "explanation": choice.explanation,
        "new_points": progress.points,
        "new_level": progress.level,
        "new_badges": new_badges,
    }
