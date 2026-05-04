from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AIExtractionResult(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    language: str | None = None
    seniority: str | None = None
    remote_type: str | None = None
    employment_type: str | None = None

    skills: list[str] = Field(default_factory=list)
    description: str | None = None

    confidence: float | None = None
    warnings: list[str] = Field(default_factory=list)


class AIExtractionError(BaseModel):
    message: str
    details: dict[str, Any] | None = None


class JobDraftCreate(BaseModel):
    raw_job_id: int

    title: str | None = None
    company: str | None = None
    location: str | None = None
    language: str | None = None
    seniority: str | None = None
    remote_type: str | None = None
    employment_type: str | None = None

    skills: list[str] = Field(default_factory=list)
    description: str | None = None

    ai_model: str | None = None
    ai_confidence: float | None = None
    ai_warnings: list[str] = Field(default_factory=list)

    extraction_status: str = "draft"


class JobDraftUpdate(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    language: str | None = None
    seniority: str | None = None
    remote_type: str | None = None
    employment_type: str | None = None

    skills: list[str] | None = None
    description: str | None = None

    ai_confidence: float | None = None
    ai_warnings: list[str] | None = None
    extraction_status: str | None = None


class JobDraftResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    raw_job_id: int

    title: str | None = None
    company: str | None = None
    location: str | None = None
    language: str | None = None
    seniority: str | None = None
    remote_type: str | None = None
    employment_type: str | None = None

    skills: list[str]
    description: str | None = None

    ai_model: str | None = None
    ai_confidence: float | None = None
    ai_warnings: list[str]

    extraction_status: str

    created_at: datetime
    updated_at: datetime