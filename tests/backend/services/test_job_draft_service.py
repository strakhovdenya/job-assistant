import pytest
from sqlalchemy.orm import Session

from app.core.job_statuses import JOB_DRAFT_STATUS_ACCEPTED
from app.models.job_draft import JobDraft
from app.models.raw_job import RawJob
from app.services.job_draft_service import JobDraftService


def create_raw_job(db: Session) -> RawJob:
    raw_job = RawJob(
        raw_text="Python developer needed",
        source="test",
        content_hash="hash-draft-service",
    )

    db.add(raw_job)
    db.commit()
    db.refresh(raw_job)

    return raw_job


def create_job_draft(db: Session) -> JobDraft:
    raw_job = create_raw_job(db)

    draft = JobDraft(
        raw_job_id=raw_job.id,
        title="Backend Developer",
        company="Test Company",
        location="Berlin",
        language="en",
        seniority="middle",
        remote_type="remote",
        employment_type="full_time",
        skills=["python", "fastapi"],
        description="Build APIs",
        extraction_status="draft",
    )

    db.add(draft)
    db.commit()
    db.refresh(draft)

    return draft


def test_get_job_draft_success(db: Session):
    draft = create_job_draft(db)

    service = JobDraftService(db)

    result = service.get_job_draft(draft.id)

    assert result.id == draft.id
    assert result.title == "Backend Developer"


def test_get_job_draft_not_found(db: Session):
    service = JobDraftService(db)

    with pytest.raises(ValueError):
        service.get_job_draft(999)


def test_update_job_draft_success(db: Session):
    draft = create_job_draft(db)

    service = JobDraftService(db)

    from app.schemas.job_draft import JobDraftUpdate

    result = service.update_job_draft(
        draft.id,
        JobDraftUpdate(
            title="Senior Backend Developer",
            skills=["python", "fastapi", "postgresql"],
        ),
    )

    assert result.title == "Senior Backend Developer"
    assert result.skills == ["python", "fastapi", "postgresql"]


def test_accept_job_draft_creates_job(db: Session):
    draft = create_job_draft(db)

    service = JobDraftService(db)

    job = service.accept_job_draft(draft.id)

    assert job.id is not None
    assert job.raw_job_id == draft.raw_job_id
    assert job.title == draft.title
    assert job.company == draft.company
    assert job.location == draft.location
    assert job.language == draft.language
    assert job.seniority == draft.seniority
    assert job.remote_type == draft.remote_type
    assert job.employment_type == draft.employment_type
    assert job.skills == draft.skills
    assert job.skills_source == "ai_reviewed"
    assert job.description == draft.description


def test_accept_job_draft_marks_draft_as_accepted(db: Session):
    draft = create_job_draft(db)

    service = JobDraftService(db)

    service.accept_job_draft(draft.id)

    refreshed = service.get_job_draft(draft.id)

    assert refreshed.extraction_status == JOB_DRAFT_STATUS_ACCEPTED


def test_accept_job_draft_twice_fails(db: Session):
    draft = create_job_draft(db)

    service = JobDraftService(db)

    service.accept_job_draft(draft.id)

    with pytest.raises(ValueError):
        service.accept_job_draft(draft.id)

def test_update_job_draft_partial_update(db: Session):
    draft = create_job_draft(db)
    service = JobDraftService(db)

    from app.schemas.job_draft import JobDraftUpdate

    result = service.update_job_draft(
        draft.id,
        JobDraftUpdate(title="Updated Title"),
    )

    assert result.title == "Updated Title"
    assert result.company == "Test Company"
    assert result.location == "Berlin"
    assert result.skills == ["python", "fastapi"]

def test_accept_job_draft_creates_job_with_correct_fields(db: Session):
    draft = create_job_draft(db)
    service = JobDraftService(db)

    job = service.accept_job_draft(draft.id)

    assert job.raw_job_id == draft.raw_job_id
    assert job.title == draft.title
    assert job.company == draft.company
    assert job.location == draft.location
    assert job.language == draft.language
    assert job.seniority == draft.seniority
    assert job.remote_type == draft.remote_type
    assert job.employment_type == draft.employment_type
    assert job.skills == draft.skills
    assert job.skills_source == "ai_reviewed"
    assert job.description == draft.description

def test_accept_job_draft_raises_for_nonexistent_draft(db: Session):
    service = JobDraftService(db)

    with pytest.raises(ValueError):
        service.accept_job_draft(999)