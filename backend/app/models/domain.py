from __future__ import annotations

import enum
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class UserRole(str, enum.Enum):
    ATHLETE = "athlete"
    COACH = "coach"
    PARENT = "parent"
    PSYCHOLOGIST = "psychologist"
    ADMIN = "admin"


class ScenarioKind(str, enum.Enum):
    PRESTART = "prestart"
    DEFEAT = "defeat"
    CONFLICT = "conflict"
    JUDGEMENT = "judgement"
    INJURY = "injury"


class MiniGameType(str, enum.Enum):
    FOCUS = "focus"
    VISUALIZATION = "visualization"
    STRESS = "stress"
    REGULATION = "regulation"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(length=320), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(length=255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    progress: Mapped["Progress | None"] = relationship(
        "Progress", back_populates="user", uselist=False
    )
    mini_game_results: Mapped[list["MiniGameResult"]] = relationship(
        "MiniGameResult", back_populates="user", cascade="all, delete-orphan"
    )
    enrollments: Mapped[list["CourseEnrollment"]] = relationship(
        "CourseEnrollment", back_populates="user", cascade="all, delete-orphan"
    )


class Scenario(Base):
    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    kind: Mapped[ScenarioKind] = mapped_column(Enum(ScenarioKind, name="scenario_kind"), nullable=False)
    content_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    role_scope: Mapped[UserRole | None] = mapped_column(
        Enum(UserRole, name="scenario_role_scope"), nullable=True
    )

    choices: Mapped[list["Choice"]] = relationship(
        "Choice", back_populates="scenario", cascade="all, delete-orphan"
    )


class Choice(Base):
    __tablename__ = "choices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id", ondelete="CASCADE"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    skill_tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    score_delta: Mapped[int] = mapped_column(Integer, nullable=False)

    scenario: Mapped[Scenario] = relationship("Scenario", back_populates="choices")


class Progress(Base):
    __tablename__ = "progress"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    points: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")
    badges: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)

    user: Mapped[User] = relationship("User", back_populates="progress")


class MiniGameResult(Base):
    __tablename__ = "mini_game_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type: Mapped[MiniGameType] = mapped_column(
        Enum(MiniGameType, name="mini_game_type"), nullable=False
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    user: Mapped[User] = relationship("User", back_populates="mini_game_results")


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    lessons: Mapped[list["CourseLesson"]] = relationship(
        "CourseLesson", back_populates="course", cascade="all, delete-orphan"
    )
    enrollments: Mapped[list["CourseEnrollment"]] = relationship(
        "CourseEnrollment", back_populates="course", cascade="all, delete-orphan"
    )


class CourseLesson(Base):
    __tablename__ = "course_lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    body_md: Mapped[str] = mapped_column(Text, nullable=False)

    course: Mapped[Course] = relationship("Course", back_populates="lessons")


class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"
    __table_args__ = (
        UniqueConstraint("user_id", "course_id", name="uq_course_enrollments_user_course"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    user: Mapped[User] = relationship("User", back_populates="enrollments")
    course: Mapped[Course] = relationship("Course", back_populates="enrollments")
