from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job_draft import JobDraft
from app.schemas.job_draft import JobDraftCreate


class JobDraftRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, job_draft_id: int) -> JobDraft | None:
        stmt = select(JobDraft).where(JobDraft.id == job_draft_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_raw_job_id(self, raw_job_id: int) -> JobDraft | None:
        stmt = select(JobDraft).where(JobDraft.raw_job_id == raw_job_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, data: JobDraftCreate) -> JobDraft:
        job_draft = JobDraft(**data.model_dump())

        self.db.add(job_draft)
        self.db.commit()
        self.db.refresh(job_draft)

        return job_draft