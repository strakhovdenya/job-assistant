"""init jobs schema

Revision ID: 26877f091945
Revises:
Create Date: 2026-04-29 20:34:21.878916

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "26877f091945"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "jobs_raw",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("raw_text", sa.Text(), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column(
            "processing_status",
            sa.String(length=50),
            server_default="raw",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("content_hash"),
    )

    op.create_index(
        op.f("ix_jobs_raw_id"),
        "jobs_raw",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_jobs_raw_content_hash"),
        "jobs_raw",
        ["content_hash"],
        unique=False,
    )

    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("raw_job_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("company", sa.String(length=255), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("language", sa.String(length=20), nullable=True),
        sa.Column("seniority", sa.String(length=50), nullable=True),
        sa.Column("remote_type", sa.String(length=50), nullable=True),
        sa.Column("employment_type", sa.String(length=50), nullable=True),
        sa.Column(
            "status",
            sa.String(length=50),
            server_default="new",
            nullable=False,
        ),
        sa.Column(
            "skills",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "skills_source",
            sa.String(length=50),
            server_default="manual",
            nullable=False,
        ),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["raw_job_id"], ["jobs_raw.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_jobs_id"),
        "jobs",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_jobs_raw_job_id"),
        "jobs",
        ["raw_job_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_jobs_raw_job_id"), table_name="jobs")
    op.drop_index(op.f("ix_jobs_id"), table_name="jobs")
    op.drop_table("jobs")

    op.drop_index(op.f("ix_jobs_raw_content_hash"), table_name="jobs_raw")
    op.drop_index(op.f("ix_jobs_raw_id"), table_name="jobs_raw")
    op.drop_table("jobs_raw")