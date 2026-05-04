"""create job_drafts table

Revision ID: 20260504_0001
Revises: <PUT_PREVIOUS_REVISION_ID_HERE>
Create Date: 2026-05-04
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260504_0001"
down_revision: Union[str, None] = "26877f091945"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "job_drafts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("raw_job_id", sa.Integer(), nullable=False),

        sa.Column("title", sa.String(), nullable=True),
        sa.Column("company", sa.String(), nullable=True),
        sa.Column("location", sa.String(), nullable=True),
        sa.Column("language", sa.String(), nullable=True),
        sa.Column("seniority", sa.String(), nullable=True),
        sa.Column("remote_type", sa.String(), nullable=True),
        sa.Column("employment_type", sa.String(), nullable=True),

        sa.Column("skills", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),

        sa.Column("ai_model", sa.String(), nullable=True),
        sa.Column("ai_confidence", sa.Float(), nullable=True),
        sa.Column("ai_warnings", postgresql.JSONB(astext_type=sa.Text()), nullable=False),

        sa.Column("extraction_status", sa.String(), nullable=False),

        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),

        sa.ForeignKeyConstraint(
            ["raw_job_id"],
            ["jobs_raw.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_job_drafts_id"),
        "job_drafts",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_job_drafts_raw_job_id"),
        "job_drafts",
        ["raw_job_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_job_drafts_raw_job_id"), table_name="job_drafts")
    op.drop_index(op.f("ix_job_drafts_id"), table_name="job_drafts")
    op.drop_table("job_drafts")