"""Factory Boy factories for domain models used in tests."""

from __future__ import annotations

import factory
from app.core.security import get_password_hash
from app.models.domain import (
    Choice,
    MiniGameResult,
    MiniGameType,
    Progress,
    Scenario,
    ScenarioKind,
    User,
    UserRole,
)
from factory.alchemy import SQLAlchemyModelFactory


class BaseFactory(SQLAlchemyModelFactory):
    """Base class that defers the SQLAlchemy session binding to fixtures."""

    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"


class UserFactory(BaseFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password_hash = factory.LazyFunction(lambda: get_password_hash("secret123"))
    role = UserRole.ATHLETE


class ProgressFactory(BaseFactory):
    class Meta:
        model = Progress

    user = factory.SubFactory(UserFactory)
    points = 0
    level = 1
    badges = factory.LazyFunction(list)


class ScenarioFactory(BaseFactory):
    class Meta:
        model = Scenario

    title = factory.Sequence(lambda n: f"Scenario {n}")
    kind = ScenarioKind.PRESTART
    content_json = factory.LazyFunction(lambda: {"body": "Focus on breathing"})
    role_scope = None

    @factory.post_generation
    def choices(
        self, create: bool, extracted: list[Choice] | None, **kwargs: object
    ) -> None:
        if not create:
            return
        if extracted:
            for choice in extracted:
                self.choices.append(choice)
        elif not self.choices:
            ChoiceFactory(scenario=self)


class ChoiceFactory(BaseFactory):
    class Meta:
        model = Choice

    scenario = factory.SubFactory(ScenarioFactory)
    text = factory.Sequence(lambda n: f"Choice {n}")
    explanation = "Deep breathing calms nerves."
    skill_tags = factory.LazyFunction(lambda: ["focus"])
    score_delta = 120


class MiniGameResultFactory(BaseFactory):
    class Meta:
        model = MiniGameResult

    user = factory.SubFactory(UserFactory)
    type = MiniGameType.FOCUS
    score = 80
