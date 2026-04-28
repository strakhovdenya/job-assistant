from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


# 🔹 Базовая схема (общие поля)
class JobBase(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None

    language: str | None = None
    seniority: str | None = None
    remote_type: str | None = None
    employment_type: str | None = None

    status: str = "new"

    skills: list[str] = []
    skills_source: str = "manual"

    description: str | None = None
    notes: str | None = None


# 🔹 Обновление (PATCH)
class JobUpdate(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None

    language: str | None = None
    seniority: str | None = None
    remote_type: str | None = None
    employment_type: str | None = None

    status: str | None = None

    skills: list[str] | None = None
    skills_source: str | None = None

    description: str | None = None
    notes: str | None = None


# 🔹 Ответ API
class JobResponse(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    raw_job_id: int

    created_at: datetime
    updated_at: datetime