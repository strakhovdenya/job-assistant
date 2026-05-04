from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


LanguageCode = Literal["ru", "en", "de", "unknown"]
Seniority = Literal["junior", "middle", "senior", "lead", "unknown"]
RemoteType = Literal["remote", "hybrid", "office", "unknown"]
EmploymentType = Literal[
    "full_time",
    "part_time",
    "contract",
    "freelance",
    "internship",
    "unknown",
]
JobDraftStatus = Literal["draft", "failed", "reviewed", "saved"]


def normalize_skill(skill: str) -> str:
    return skill.strip().lower()


class AIExtractionResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str | None = None
    company: str | None = None
    location: str | None = None
    language: LanguageCode | None = None
    seniority: Seniority | None = None
    remote_type: RemoteType | None = None
    employment_type: EmploymentType | None = None

    skills: list[str] = Field(default_factory=list)
    description: str | None = None

    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    warnings: list[str] = Field(default_factory=list)

    @field_validator("skills")
    @classmethod
    def validate_skills(cls, value: list[str]) -> list[str]:
        normalized = []

        for skill in value:
            if not isinstance(skill, str):
                continue

            normalized_skill = normalize_skill(skill)

            if normalized_skill and normalized_skill not in normalized:
                normalized.append(normalized_skill)

        return normalized


class AIExtractionError(BaseModel):
    message: str
    details: dict[str, Any] | None = None


class JobDraftCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    raw_job_id: int

    title: str | None = None
    company: str | None = None
    location: str | None = None
    language: LanguageCode | None = None
    seniority: Seniority | None = None
    remote_type: RemoteType | None = None
    employment_type: EmploymentType | None = None

    skills: list[str] = Field(default_factory=list)
    description: str | None = None

    ai_model: str | None = None
    ai_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    ai_warnings: list[str] = Field(default_factory=list)

    extraction_status: JobDraftStatus = "draft"

    @field_validator("skills")
    @classmethod
    def validate_skills(cls, value: list[str]) -> list[str]:
        normalized = []

        for skill in value:
            if not isinstance(skill, str):
                continue

            normalized_skill = normalize_skill(skill)

            if normalized_skill and normalized_skill not in normalized:
                normalized.append(normalized_skill)

        return normalized


class JobDraftUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str | None = None
    company: str | None = None
    location: str | None = None
    language: LanguageCode | None = None
    seniority: Seniority | None = None
    remote_type: RemoteType | None = None
    employment_type: EmploymentType | None = None

    skills: list[str] | None = None
    description: str | None = None

    ai_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    ai_warnings: list[str] | None = None
    extraction_status: JobDraftStatus | None = None

    @field_validator("skills")
    @classmethod
    def validate_skills(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return None

        normalized = []

        for skill in value:
            if not isinstance(skill, str):
                continue

            normalized_skill = normalize_skill(skill)

            if normalized_skill and normalized_skill not in normalized:
                normalized.append(normalized_skill)

        return normalized


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