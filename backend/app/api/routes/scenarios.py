"""Endpoints for interactive scenarios and choice handling."""

from __future__ import annotations

from app.api import deps
from app.db.session import get_db
from app.models.domain import Choice, Scenario, ScenarioKind, User, UserRole
from app.schemas import (
    ChoiceApplyRequest,
    ChoiceApplyResponse,
    ScenarioCreate,
    ScenarioDetail,
)
from app.services import apply_effect
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


@router.get("", response_model=list[ScenarioDetail], summary="List scenarios")
def list_scenarios(
    *,
    role: UserRole | None = Query(
        default=None,
        description=(
            "Filter scenarios by role scope. "
            "Scenarios available to all roles are always included."
        ),
    ),
    kind: ScenarioKind | None = Query(
        default=None, description="Filter scenarios by their thematic kind."
    ),
    db: Session = Depends(get_db),
) -> list[ScenarioDetail]:
    """Return scenarios optionally filtered by role and kind."""

    stmt = select(Scenario).options(joinedload(Scenario.choices))
    if role is not None:
        stmt = stmt.where(
            or_(Scenario.role_scope.is_(None), Scenario.role_scope == role)
        )
    if kind is not None:
        stmt = stmt.where(Scenario.kind == kind)

    result = db.execute(stmt.order_by(Scenario.id))
    scenarios = result.unique().scalars().all()
    return [ScenarioDetail.model_validate(scenario) for scenario in scenarios]


@router.get(
    "/{scenario_id}",
    response_model=ScenarioDetail,
    summary="Retrieve a scenario by ID",
)
def get_scenario(
    *,
    scenario_id: int,
    db: Session = Depends(get_db),
) -> ScenarioDetail:
    """Return a single scenario with its choices."""

    scenario = db.execute(
        select(Scenario)
        .options(joinedload(Scenario.choices))
        .where(Scenario.id == scenario_id)
    ).scalar_one_or_none()
    if scenario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found."
        )

    return ScenarioDetail.model_validate(scenario)


@router.post(
    "",
    response_model=ScenarioDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new scenario",
)
def create_scenario(
    *,
    payload: ScenarioCreate,
    db: Session = Depends(get_db),
    _: User = Depends(deps.require_roles(UserRole.ADMIN)),
) -> ScenarioDetail:
    """Create a scenario along with its choices."""

    scenario = Scenario(
        title=payload.title,
        kind=payload.kind,
        content_json=payload.content_json,
        role_scope=payload.role_scope,
    )

    for choice_payload in payload.choices:
        scenario.choices.append(
            Choice(
                text=choice_payload.text,
                explanation=choice_payload.explanation,
                skill_tags=choice_payload.skill_tags,
                score_delta=choice_payload.score_delta,
            )
        )

    db.add(scenario)
    db.commit()
    db.refresh(scenario)

    return ScenarioDetail.model_validate(scenario)


@router.post(
    "/{scenario_id}/choice",
    response_model=ChoiceApplyResponse,
    summary="Apply a choice to the current user's progress",
)
def apply_choice(
    *,
    scenario_id: int,
    payload: ChoiceApplyRequest,
    db: Session = Depends(get_db),
    user: User = Depends(deps.get_current_user),
) -> ChoiceApplyResponse:
    """Apply the selected choice to the user's progress and return the outcome."""

    choice = db.execute(
        select(Choice).where(
            Choice.id == payload.choice_id,
            Choice.scenario_id == scenario_id,
        )
    ).scalar_one_or_none()

    if choice is None:
        # Ensure the scenario exists before returning 404 for missing choice.
        scenario_exists = db.get(Scenario, scenario_id)
        if scenario_exists is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scenario not found.",
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Choice not found for the provided scenario.",
        )

    result = apply_effect(user.id, choice, db=db)
    return ChoiceApplyResponse(**result)
