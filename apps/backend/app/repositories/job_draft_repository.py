from sqlalchemy import desc, select
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

    def list_by_raw_job_id(self, raw_job_id: int) -> list[JobDraft]:
        stmt = (
            select(JobDraft)
            .where(JobDraft.raw_job_id == raw_job_id)
            .order_by(desc(JobDraft.created_at))
        )

        return list(self.db.execute(stmt).scalars().all())

    def create(self, data: JobDraftCreate) -> JobDraft:
        job_draft = JobDraft(**data.model_dump())

        self.db.add(job_draft)
        self.db.commit()
        self.db.refresh(job_draft)

        return job_draft