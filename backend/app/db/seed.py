"""Seed helpers for demo scenarios, course content and admin account."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.domain import (
    Choice,
    Course,
    CourseLesson,
    Scenario,
    ScenarioKind,
    User,
    UserRole,
)


@dataclass(frozen=True)
class ChoiceData:
    text: str
    explanation: str
    skill_tags: list[str]
    score_delta: int


@dataclass(frozen=True)
class ScenarioData:
    title: str
    kind: ScenarioKind
    content_json: dict[str, object]
    choices: tuple[ChoiceData, ChoiceData, ChoiceData]


@dataclass(frozen=True)
class LessonData:
    title: str
    body_md: str


@dataclass(frozen=True)
class CourseData:
    title: str
    description: str
    lessons: tuple[LessonData, ...]


ADMIN_EMAIL = "admin@local"
ADMIN_PASSWORD = "admin"

SCENARIOS: tuple[ScenarioData, ...] = (
    ScenarioData(
        title="Дыхание перед стартом",
        kind=ScenarioKind.PRESTART,
        content_json={
            "summary": "Финал турнира, спортсмен ощущает резкий подъем тревоги перед выходом на площадку.",
            "prompt": "Тренер просит тебя настроиться и сосредоточиться на своих действиях в первые минуты матча.",
        },
        choices=(
            ChoiceData(
                text="Сделать три цикла дыхания 4-4-6 и проговорить внутреннюю установку",
                explanation="Ритмичное дыхание и позитивная установка активируют парасимпатическую систему и снижают напряжение.",
                skill_tags=["дыхание", "позитивный_саморазговор"],
                score_delta=3,
            ),
            ChoiceData(
                text="Срочно пролистать телефон, чтобы отвлечься от тревоги",
                explanation="Цифровые раздражители усиливают перевозбуждение и мешают телу почувствовать контроль.",
                skill_tags=["самоконтроль"],
                score_delta=-1,
            ),
            ChoiceData(
                text="Начать разминку в высоком темпе без плана",
                explanation="Хаотичные действия повышают частоту сердечных сокращений и не дают мозгу структурироваться.",
                skill_tags=["организация"],
                score_delta=-2,
            ),
        ),
    ),
    ScenarioData(
        title="После поражения",
        kind=ScenarioKind.DEFEAT,
        content_json={
            "summary": "Матч проигран, команда молчит, а тренер ждёт твоей реакции.",
            "prompt": "Нужно выбрать первый шаг, который поможет прожить эмоции и сделать выводы.",
        },
        choices=(
            ChoiceData(
                text="Признать свои чувства, обсудить с тренером ключевой эпизод и запланировать восстановление",
                explanation="Осознанное проживание эмоций и анализ поддерживают чувство контроля и ускоряют обучение.",
                skill_tags=["эмоциональная_осознанность", "анализ"],
                score_delta=3,
            ),
            ChoiceData(
                text="Замкнуться и обвинить себя при всей команде",
                explanation="Самокритика без анализа закрепляет ощущение беспомощности и снижает мотивацию.",
                skill_tags=["самоподдержка"],
                score_delta=-2,
            ),
            ChoiceData(
                text="Перевести разговор на судей и внешние обстоятельства",
                explanation="Смещение ответственности мешает заметить зоны роста и повторно исправить ошибку.",
                skill_tags=["ответственность"],
                score_delta=-1,
            ),
        ),
    ),
    ScenarioData(
        title="Конфликт с партнёром",
        kind=ScenarioKind.CONFLICT,
        content_json={
            "summary": "Во время тренировки партнёр раздражён, считает, что ты не выкладываешься.",
            "prompt": "Нужно выбрать реакцию, чтобы сохранить рабочие отношения и командный настрой.",
        },
        choices=(
            ChoiceData(
                text="Описать наблюдаемые факты, услышать партнёра и предложить распределить роли",
                explanation="Ассертивное общение и уточнение ожиданий уменьшают напряжение и возвращают фокус на задачу.",
                skill_tags=["коммуникация", "ассертивность"],
                score_delta=3,
            ),
            ChoiceData(
                text="Отмахнуться и продолжить молча делать упражнение",
                explanation="Игнорирование усиливает конфликт и не даёт партнёру почувствовать сотрудничество.",
                skill_tags=["эмпатия"],
                score_delta=-1,
            ),
            ChoiceData(
                text="Ответить агрессивно и напомнить о его прошлых ошибках",
                explanation="Атака в ответ разрушает доверие и переводит внимание с тренировки на выяснение отношений.",
                skill_tags=["управление_эмоциями"],
                score_delta=-3,
            ),
        ),
    ),
)

COURSE = CourseData(
    title="Как справиться с волнением перед стартом",
    description=(
        "Практический курс для спортсменов и тренеров, который помогает снизить тревогу перед соревнованиями,"
        " настроить тело и внимание на первые минуты выступления."
    ),
    lessons=(
        LessonData(
            title="Осознанное дыхание перед выходом",
            body_md=(
                "Разберём технику дыхания 4-4-6 и подготовим персональную фразу поддержки."
                " Выполните три подхода дыхания и запишите ощущения."
            ),
        ),
        LessonData(
            title="Ментальная репетиция старта",
            body_md=(
                "Представьте первые 90 секунд выступления во всех деталях: звук, дыхание, движения."
                " Запишите, какие моменты вызывают напряжение и какие фразы помогают возвращаться в ритм."
            ),
        ),
        LessonData(
            title="Ритуал концентрации",
            body_md=(
                "Сформируйте личный ритуал из трёх шагов: действие тела, настройка внимания и проверка целей."
                " Опишите план и протестируйте его на ближайшей тренировке."
            ),
        ),
    ),
)


def get_or_create_admin(session: Session) -> User:
    user = session.scalar(select(User).where(User.email == ADMIN_EMAIL))
    if user:
        return user

    user = User(
        email=ADMIN_EMAIL,
        password_hash=get_password_hash(ADMIN_PASSWORD),
        role=UserRole.ADMIN,
    )
    session.add(user)
    session.flush()
    return user


def upsert_scenario(session: Session, data: ScenarioData) -> Scenario:
    scenario = session.scalar(select(Scenario).where(Scenario.title == data.title))
    if scenario is None:
        scenario = Scenario(
            title=data.title,
            kind=data.kind,
            content_json=data.content_json,
        )
        session.add(scenario)
    else:
        scenario.kind = data.kind
        scenario.content_json = data.content_json
        scenario.role_scope = None
        scenario.choices.clear()

    for choice_data in data.choices:
        scenario.choices.append(
            Choice(
                text=choice_data.text,
                explanation=choice_data.explanation,
                skill_tags=choice_data.skill_tags,
                score_delta=choice_data.score_delta,
            )
        )
    session.flush()
    return scenario


def upsert_course(session: Session, data: CourseData) -> Course:
    course = session.scalar(select(Course).where(Course.title == data.title))
    if course is None:
        course = Course(title=data.title, description=data.description)
        session.add(course)
    else:
        course.description = data.description
        course.lessons.clear()

    for lesson in data.lessons:
        course.lessons.append(
            CourseLesson(
                title=lesson.title,
                body_md=lesson.body_md,
            )
        )
    session.flush()
    return course


def seed() -> None:
    """Seed the database with demo data."""
    with SessionLocal() as session:
        get_or_create_admin(session)

        for scenario_data in SCENARIOS:
            upsert_scenario(session, scenario_data)

        upsert_course(session, COURSE)
        session.commit()


if __name__ == "__main__":
    seed()
    print("Seed data successfully applied.")
