"""Endpoints providing access to the player's progress."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.models.domain import Progress, User
from app.schemas import ProgressSummary

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/me", response_model=ProgressSummary, summary="Get my progress")
def get_my_progress(
    *, db: Session = Depends(get_db), user: User = Depends(deps.get_current_user)
) -> ProgressSummary:
    """Return the current user's progress summary."""

    progress = db.get(Progress, user.id)
    if progress is None:
        return ProgressSummary(points=0, level=1, badges=[])

    points = progress.points or 0
    badges = list(progress.badges or [])
    level = max(1, points // 100 + 1)

    return ProgressSummary(points=points, level=level, badges=badges)


__all__ = ["router"]
