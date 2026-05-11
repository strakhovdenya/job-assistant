from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.models.job_draft import JobDraft
from app.models.raw_job import RawJob
from app.repositories.job_draft_repository import JobDraftRepository
from app.schemas.job_draft import JobDraftCreate


def create_raw_job(db: Session, content_hash: str = "hash-job-draft-repo") -> RawJob:
    raw_job = RawJob(
        raw_text="Python developer needed",
        source="test",
        content_hash=content_hash,
    )

    db.add(raw_job)
    db.commit()
    db.refresh(raw_job)

    return raw_job


def test_job_draft_repository_create(db: Session):
    raw_job = create_raw_job(db, content_hash="hash-draft-create")
    repository = JobDraftRepository(db)

    draft = repository.create(
        JobDraftCreate(
            raw_job_id=raw_job.id,
            title="Backend Developer",
            company="Acme",
            location="Berlin",
            language="en",
            seniority="middle",
            remote_type="remote",
            employment_type="full_time",
            skills=["python", "fastapi"],
            description="Build APIs",
            ai_confidence=0.9,
            ai_warnings=[],
            extraction_status="draft",
        )
    )

    assert draft.id is not None
    assert draft.raw_job_id == raw_job.id
    assert draft.title == "Backend Developer"
    assert draft.company == "Acme"
    assert draft.skills == ["python", "fastapi"]
    assert draft.extraction_status == "draft"


def test_job_draft_repository_get_by_id(db: Session):
    raw_job = create_raw_job(db, content_hash="hash-draft-get-by-id")
    repository = JobDraftRepository(db)

    draft = repository.create(
        JobDraftCreate(
            raw_job_id=raw_job.id,
            title="Backend Developer",
            skills=[],
            extraction_status="draft",
        )
    )

    result = repository.get_by_id(draft.id)

    assert result is not None
    assert result.id == draft.id
    assert result.raw_job_id == raw_job.id
    assert result.title == "Backend Developer"


def test_job_draft_repository_get_by_id_returns_none_for_missing_id(db: Session):
    repository = JobDraftRepository(db)

    result = repository.get_by_id(999)

    assert result is None


def test_job_draft_repository_get_by_raw_job_id(db: Session):
    raw_job = create_raw_job(db, content_hash="hash-draft-get-by-raw")
    repository = JobDraftRepository(db)

    draft = repository.create(
        JobDraftCreate(
            raw_job_id=raw_job.id,
            title="Draft for RawJob",
            skills=[],
            extraction_status="draft",
        )
    )

    result = repository.get_by_raw_job_id(raw_job.id)

    assert result is not None
    assert result.id == draft.id
    assert result.raw_job_id == raw_job.id


def test_job_draft_repository_get_by_raw_job_id_returns_none_for_missing_raw_job(
    db: Session,
):
    repository = JobDraftRepository(db)

    result = repository.get_by_raw_job_id(999)

    assert result is None


def test_job_draft_repository_list_by_raw_job_id_returns_only_matching_drafts(
    db: Session,
):
    first_raw_job = create_raw_job(db, content_hash="hash-draft-list-first")
    second_raw_job = create_raw_job(db, content_hash="hash-draft-list-second")

    first_draft = JobDraft(
        raw_job_id=first_raw_job.id,
        title="First RawJob Draft",
        skills=[],
        extraction_status="draft",
    )

    second_draft = JobDraft(
        raw_job_id=second_raw_job.id,
        title="Second RawJob Draft",
        skills=[],
        extraction_status="draft",
    )

    db.add_all([first_draft, second_draft])
    db.commit()

    repository = JobDraftRepository(db)

    result = repository.list_by_raw_job_id(first_raw_job.id)

    assert len(result) == 1
    assert result[0].title == "First RawJob Draft"
    assert result[0].raw_job_id == first_raw_job.id


def test_job_draft_repository_list_by_raw_job_id_empty_and_ordering(db: Session):
    raw_job = create_raw_job(db, content_hash="hash-list-by-raw-job-ordering")

    repository = JobDraftRepository(db)

    assert repository.list_by_raw_job_id(raw_job.id) == []

    older_draft = JobDraft(
        raw_job_id=raw_job.id,
        title="Older Draft",
        skills=[],
        extraction_status="draft",
        created_at=datetime.now(UTC) - timedelta(days=1),
    )

    newer_draft = JobDraft(
        raw_job_id=raw_job.id,
        title="Newer Draft",
        skills=[],
        extraction_status="draft",
        created_at=datetime.now(UTC),
    )

    db.add_all([older_draft, newer_draft])
    db.commit()

    result = repository.list_by_raw_job_id(raw_job.id)

    assert [draft.title for draft in result] == [
        "Newer Draft",
        "Older Draft",
    ]


def test_job_draft_repository_list_by_raw_job_id_returns_empty_list_for_missing_raw_job(
    db: Session,
):
    repository = JobDraftRepository(db)

    result = repository.list_by_raw_job_id(999)

    assert result == []