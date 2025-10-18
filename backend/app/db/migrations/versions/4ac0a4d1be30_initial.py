"""Initial domain models

Revision ID: 4ac0a4d1be30
Revises: 
Create Date: 2024-06-01 00:00:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import ENUM as PGEnum


# revision identifiers, used by Alembic.
revision = "4ac0a4d1be30"
down_revision = None
branch_labels = None
depends_on = None


user_role_enum = PGEnum(
    "athlete", "coach", "parent", "psychologist", "admin", name="user_role", create_type=False
)
scenario_kind_enum = PGEnum(
    "prestart", "defeat", "conflict", "judgement", "injury", name="scenario_kind", create_type=False
)
scenario_role_scope_enum = PGEnum(
    "athlete", "coach", "parent", "psychologist", "admin", name="scenario_role_scope", create_type=False
)
mini_game_type_enum = PGEnum(
    "focus", "visualization", "stress", "regulation", name="mini_game_type", create_type=False
)


def upgrade() -> None:
    bind = op.get_bind()
    bind.execute(
        text(
            """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
                CREATE TYPE user_role AS ENUM ('athlete','coach','parent','psychologist','admin');
            END IF;
        END$$;
        """
        )
    )
    bind.execute(
        text(
            """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'scenario_kind') THEN
                CREATE TYPE scenario_kind AS ENUM ('prestart','defeat','conflict','judgement','injury');
            END IF;
        END$$;
        """
        )
    )
    bind.execute(
        text(
            """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'scenario_role_scope') THEN
                CREATE TYPE scenario_role_scope AS ENUM ('athlete','coach','parent','psychologist','admin');
            END IF;
        END$$;
        """
        )
    )
    bind.execute(
        text(
            """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'mini_game_type') THEN
                CREATE TYPE mini_game_type AS ENUM ('focus','visualization','stress','regulation');
            END IF;
        END$$;
        """
        )
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", user_role_enum, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    op.create_table(
        "scenarios",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("kind", scenario_kind_enum, nullable=False),
        sa.Column("content_json", sa.JSON(), nullable=False),
        sa.Column("role_scope", scenario_role_scope_enum, nullable=True),
    )

    op.create_table(
        "progress",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("points", sa.Integer(), server_default="0", nullable=False),
        sa.Column("level", sa.Integer(), server_default="1", nullable=False),
        sa.Column("badges", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
    )

    op.create_table(
        "courses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
    )

    op.create_table(
        "course_enrollments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id", "course_id", name="uq_course_enrollments_user_course"),
    )

    op.create_table(
        "course_lessons",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("body_md", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "mini_game_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("type", mini_game_type_enum, nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "choices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("scenario_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("skill_tags", sa.JSON(), nullable=False),
        sa.Column("score_delta", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["scenario_id"], ["scenarios.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("choices")
    op.drop_table("mini_game_results")
    op.drop_table("course_lessons")
    op.drop_table("course_enrollments")
    op.drop_table("courses")
    op.drop_table("progress")
    op.drop_table("scenarios")
    op.drop_table("users")

    bind = op.get_bind()
    bind.execute(text("DROP TYPE IF EXISTS mini_game_type CASCADE;"))
    bind.execute(text("DROP TYPE IF EXISTS scenario_role_scope CASCADE;"))
    bind.execute(text("DROP TYPE IF EXISTS scenario_kind CASCADE;"))
    bind.execute(text("DROP TYPE IF EXISTS user_role CASCADE;"))
