from sqlalchemy.orm import Session

from app.core.job_statuses import JOB_DRAFT_STATUS_ACCEPTED
from app.models.job import Job
from app.models.job_draft import JobDraft
from app.repositories.job_draft_repository import JobDraftRepository
from app.schemas.job_draft import JobDraftUpdate
from app.services.errors import NotFoundError, ConflictError


class JobDraftService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = JobDraftRepository(db)

    def get_job_draft(self, job_draft_id: int) -> JobDraft:
        job_draft = self.repository.get_by_id(job_draft_id)

        if job_draft is None:
            raise NotFoundError(f"JobDraft with id={job_draft_id} not found")

        return job_draft

    def update_job_draft(
        self,
        job_draft_id: int,
        payload: JobDraftUpdate,
    ) -> JobDraft:
        job_draft = self.get_job_draft(job_draft_id)

        update_data = payload.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(job_draft, field, value)

        self.db.add(job_draft)
        self.db.commit()
        self.db.refresh(job_draft)

        return job_draft

    def accept_job_draft(self, job_draft_id: int) -> Job:
        job_draft = self.get_job_draft(job_draft_id)

        if job_draft.extraction_status == JOB_DRAFT_STATUS_ACCEPTED:
            raise ConflictError("JobDraft already accepted")

        job = Job(
            raw_job_id=job_draft.raw_job_id,
            title=job_draft.title,
            company=job_draft.company,
            location=job_draft.location,
            language=job_draft.language,
            seniority=job_draft.seniority,
            remote_type=job_draft.remote_type,
            employment_type=job_draft.employment_type,
            skills=job_draft.skills,
            skills_source="ai_reviewed",
            description=job_draft.description,
        )

        job_draft.extraction_status = JOB_DRAFT_STATUS_ACCEPTED

        self.db.add(job)
        self.db.add(job_draft)
        self.db.commit()
        self.db.refresh(job)

        return job

