"""Endpoints for managing mini-game results."""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.models.domain import MiniGameResult, MiniGameType, Progress, User
from app.schemas import (
    MiniGameResultCreateRequest,
    MiniGameResultRead,
    MiniGameResultResponse,
    ProgressSummary,
)

router = APIRouter(prefix="/minigames", tags=["minigames"])


@router.post(
    "/{mini_game_type}/result",
    response_model=MiniGameResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit mini-game result",
)
def submit_mini_game_result(
    *,
    mini_game_type: MiniGameType,
    payload: MiniGameResultCreateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(deps.get_current_user),
) -> MiniGameResultResponse:
    """Store a mini-game result and update the user's progress."""

    progress = db.get(Progress, user.id)
    if progress is None:
        progress = Progress(user_id=user.id, points=0, level=1, badges=[])
        db.add(progress)

    result = MiniGameResult(user_id=user.id, type=mini_game_type, score=payload.score)
    db.add(result)

    current_points = progress.points or 0
    new_points = current_points + payload.score
    progress.points = new_points
    progress.level = max(1, new_points // 100 + 1)

    badges = list(progress.badges or [])

    db.flush()

    total_score = db.scalar(
        select(func.sum(MiniGameResult.score)).where(MiniGameResult.user_id == user.id)
    )
    total_score = int(total_score or 0)

    mastery_badge = "Мастер концентрации"
    if total_score > 300 and mastery_badge not in badges:
        badges.append(mastery_badge)

    progress.badges = badges

    db.commit()
    db.refresh(result)
    db.refresh(progress)

    return MiniGameResultResponse(
        result=MiniGameResultRead.model_validate(result),
        progress=ProgressSummary(
            points=progress.points,
            level=max(1, progress.points // 100 + 1),
            badges=list(progress.badges or []),
        ),
    )


__all__ = ["router"]
