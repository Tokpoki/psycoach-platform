from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field

from app.models.domain import MiniGameType, ScenarioKind, UserRole


class ORMModel(BaseModel):
    """Base schema configured for ORM mode."""

    model_config = dict(from_attributes=True)


class UserWrite(ORMModel):
    email: EmailStr
    password_hash: str = Field(min_length=1)
    role: UserRole


class UserRead(UserWrite):
    id: int
    created_at: datetime


class UserPublic(ORMModel):
    id: int
    email: EmailStr
    role: UserRole
    created_at: datetime


class ScenarioWrite(ORMModel):
    title: str = Field(min_length=1)
    kind: ScenarioKind
    content_json: dict[str, Any]
    role_scope: UserRole | None = None


class ScenarioRead(ScenarioWrite):
    id: int


class ChoiceCreate(BaseModel):
    text: str = Field(min_length=1)
    explanation: str = Field(min_length=1)
    skill_tags: list[str] = Field(default_factory=list)
    score_delta: int


class ScenarioCreate(ScenarioWrite):
    choices: list[ChoiceCreate] = Field(default_factory=list)


class ChoiceWrite(ORMModel):
    scenario_id: int
    text: str
    explanation: str
    skill_tags: list[str] = Field(default_factory=list)
    score_delta: int


class ChoiceRead(ChoiceWrite):
    id: int


class ScenarioDetail(ScenarioRead):
    choices: list[ChoiceRead] = Field(default_factory=list)


class ChoiceApplyRequest(BaseModel):
    choice_id: int


class ChoiceApplyResponse(BaseModel):
    applied_skill: list[str]
    explanation: str
    new_points: int
    new_level: int
    new_badges: list[str]


class ProgressWrite(ORMModel):
    user_id: int
    points: int = 0
    level: int = 1
    badges: list[str] = Field(default_factory=list)


class ProgressRead(ProgressWrite):
    pass


class MiniGameResultWrite(ORMModel):
    user_id: int
    type: MiniGameType
    score: int


class MiniGameResultRead(MiniGameResultWrite):
    id: int
    created_at: datetime


class CourseWrite(ORMModel):
    title: str = Field(min_length=1)
    description: str


class CourseRead(CourseWrite):
    id: int


class CourseLessonWrite(ORMModel):
    course_id: int
    title: str = Field(min_length=1)
    body_md: str


class CourseLessonRead(CourseLessonWrite):
    id: int


class CourseEnrollmentWrite(ORMModel):
    user_id: int
    course_id: int
    started_at: datetime | None = None


class CourseEnrollmentRead(CourseEnrollmentWrite):
    id: int
