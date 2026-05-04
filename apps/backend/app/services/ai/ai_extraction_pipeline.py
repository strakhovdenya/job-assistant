from sqlalchemy.orm import Session

from app.core.job_statuses import (
    JOB_DRAFT_STATUS_DRAFT,
    JOB_DRAFT_STATUS_FAILED,
    RAW_JOB_STATUS_AI_DRAFTED,
)
from app.models.job_draft import JobDraft
from app.repositories.job_draft_repository import JobDraftRepository
from app.repositories.raw_job_repository import RawJobRepository
from app.schemas.job_draft import JobDraftCreate
from app.services.ai.ai_client import AIClient, AIClientError
from app.services.ai.ai_client_factory import get_ai_client


class AIExtractionPipeline:
    def __init__(
        self,
        db: Session,
        ai_client: AIClient | None = None,
    ) -> None:
        self.db = db
        self.raw_job_repository = RawJobRepository(db)
        self.job_draft_repository = JobDraftRepository(db)
        self.ai_client = ai_client or get_ai_client()

    def run(self, raw_job_id: int) -> JobDraft:
        raw_job = self.raw_job_repository.get_by_id(raw_job_id)

        if raw_job is None:
            raise ValueError("RawJob not found")

        existing_draft = self.job_draft_repository.get_by_raw_job_id(raw_job_id)

        if existing_draft is not None:
            raise ValueError("JobDraft already exists for this RawJob")

        try:
            extraction = self.ai_client.extract_job(raw_job.raw_text)

            draft = self.job_draft_repository.create(
                JobDraftCreate(
                    raw_job_id=raw_job.id,
                    title=extraction.title,
                    company=extraction.company,
                    location=extraction.location,
                    language=extraction.language,
                    seniority=extraction.seniority,
                    remote_type=extraction.remote_type,
                    employment_type=extraction.employment_type,
                    skills=extraction.skills,
                    description=extraction.description,
                    ai_confidence=extraction.confidence,
                    ai_warnings=extraction.warnings,
                    extraction_status=JOB_DRAFT_STATUS_DRAFT,
                )
            )

            raw_job.processing_status = RAW_JOB_STATUS_AI_DRAFTED
            self.db.add(raw_job)
            self.db.commit()
            self.db.refresh(draft)

            return draft

        except AIClientError as exc:
            return self._create_failed_draft(
                raw_job_id=raw_job.id,
                message=str(exc),
            )

    def _create_failed_draft(self, *, raw_job_id: int, message: str) -> JobDraft:
        return self.job_draft_repository.create(
            JobDraftCreate(
                raw_job_id=raw_job_id,
                ai_warnings=[message],
                extraction_status=JOB_DRAFT_STATUS_FAILED,
            )
        )