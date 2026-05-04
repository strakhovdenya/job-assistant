import pytest
from sqlalchemy.orm import Session

from app.models.raw_job import RawJob
from app.repositories.job_draft_repository import JobDraftRepository
from app.services.ai.ai_client import AIClientError
from app.services.ai.ai_extraction_pipeline import AIExtractionPipeline


class DummyAIClient:
    def extract_job(self, raw_text: str):
        class Result:
            title = "Backend Developer"
            company = "Test Company"
            location = "Berlin"
            language = "en"
            seniority = "middle"  # ✅ FIX HERE
            remote_type = "remote"
            employment_type = "full_time"
            skills = ["python", "fastapi"]
            description = "Test description"
            confidence = 0.9
            warnings = []

        return Result()


class FailingAIClient:
    def extract_job(self, raw_text: str):
        raise AIClientError("AI failed")


def create_raw_job(db: Session) -> RawJob:
    raw_job = RawJob(
        raw_text="Some job description",
        source="test",
        content_hash="hash123",
    )
    db.add(raw_job)
    db.commit()
    db.refresh(raw_job)
    return raw_job


def test_pipeline_success(db: Session):
    raw_job = create_raw_job(db)

    pipeline = AIExtractionPipeline(
        db=db,
        ai_client=DummyAIClient(),
    )

    draft = pipeline.run(raw_job.id)

    assert draft.id is not None
    assert draft.raw_job_id == raw_job.id
    assert draft.title == "Backend Developer"
    assert draft.ai_confidence == 0.9


def test_pipeline_raw_job_not_found(db: Session):
    pipeline = AIExtractionPipeline(
        db=db,
        ai_client=DummyAIClient(),
    )

    with pytest.raises(ValueError):
        pipeline.run(999)


def test_pipeline_already_exists(db: Session):
    raw_job = create_raw_job(db)

    pipeline = AIExtractionPipeline(
        db=db,
        ai_client=DummyAIClient(),
    )

    pipeline.run(raw_job.id)

    with pytest.raises(ValueError):
        pipeline.run(raw_job.id)


def test_pipeline_ai_error_creates_failed_draft(db: Session):
    raw_job = create_raw_job(db)

    pipeline = AIExtractionPipeline(
        db=db,
        ai_client=FailingAIClient(),
    )

    draft = pipeline.run(raw_job.id)

    assert draft.raw_job_id == raw_job.id
    assert draft.extraction_status == "failed"
    assert len(draft.ai_warnings) > 0