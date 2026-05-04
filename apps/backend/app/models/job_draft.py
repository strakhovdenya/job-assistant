from datetime import datetime, UTC
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    Float,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.core.job_statuses import JOB_DRAFT_STATUS_DRAFT

from app.db.base import Base

def utc_now():
    return datetime.now(UTC)

class JobDraft(Base):
    __tablename__ = "job_drafts"

    id = Column(Integer, primary_key=True, index=True)

    raw_job_id = Column(
        Integer,
        ForeignKey("jobs_raw.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # --- extracted fields ---
    title = Column(String, nullable=True)
    company = Column(String, nullable=True)
    location = Column(String, nullable=True)
    language = Column(String, nullable=True)
    seniority = Column(String, nullable=True)
    remote_type = Column(String, nullable=True)
    employment_type = Column(String, nullable=True)

    skills = Column(JSONB, nullable=False, default=list)
    description = Column(Text, nullable=True)

    # --- AI metadata ---
    ai_model = Column(String, nullable=True)
    ai_confidence = Column(Float, nullable=True)
    ai_warnings = Column(JSONB, nullable=False, default=list)

    extraction_status = Column(
        String,
        nullable=False,
        default=JOB_DRAFT_STATUS_DRAFT,  # draft / failed / reviewed / saved
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=utc_now,
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    # --- relations ---
    raw_job = relationship("RawJob", back_populates="job_drafts")