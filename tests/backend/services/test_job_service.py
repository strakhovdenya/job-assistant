import pytest

from app.models.raw_job import RawJob
from app.schemas.job import JobUpdate
from app.services.job_service import JobService


def create_raw_job(db, raw_text="Python Developer", source="manual"):
    raw_job = RawJob(
        raw_text=raw_text,
        source=source,
        content_hash=f"hash-{raw_text}",
    )
    db.add(raw_job)
    db.commit()
    db.refresh(raw_job)
    return raw_job


def test_create_job_from_raw_creates_job(db):
    raw_job = create_raw_job(db)

    service = JobService(db)

    job = service.create_job_from_raw(raw_job.id)

    assert job.id is not None
    assert job.raw_job_id == raw_job.id
    assert job.status == "new"
    assert job.skills == []
    assert job.skills_source == "manual"
    assert job.description == raw_job.raw_text


def test_create_job_from_raw_sets_raw_job_status_to_structured(db):
    raw_job = create_raw_job(db)

    service = JobService(db)

    service.create_job_from_raw(raw_job.id)

    db.refresh(raw_job)
    assert raw_job.processing_status == "structured"


def test_create_job_from_raw_raises_when_raw_job_not_found(db):
    service = JobService(db)

    with pytest.raises(ValueError, match="RawJob not found"):
        service.create_job_from_raw(999)


def test_create_job_from_raw_raises_when_job_already_exists(db):
    raw_job = create_raw_job(db)

    service = JobService(db)
    service.create_job_from_raw(raw_job.id)

    with pytest.raises(ValueError, match="Job already exists for this RawJob"):
        service.create_job_from_raw(raw_job.id)


def test_get_job_returns_existing_job(db):
    raw_job = create_raw_job(db)

    service = JobService(db)
    created_job = service.create_job_from_raw(raw_job.id)

    job = service.get_job(created_job.id)

    assert job.id == created_job.id


def test_get_job_raises_when_not_found(db):
    service = JobService(db)

    with pytest.raises(ValueError, match="Job not found"):
        service.get_job(999)


def test_update_job_updates_fields(db):
    raw_job = create_raw_job(db)

    service = JobService(db)
    job = service.create_job_from_raw(raw_job.id)

    updated = service.update_job(
        job.id,
        JobUpdate(
            title="Backend Developer",
            company="Acme",
            skills=["Python", "FastAPI"],
            notes="Interesting role",
            status="reviewed",
        ),
    )

    assert updated.title == "Backend Developer"
    assert updated.company == "Acme"
    assert updated.skills == ["Python", "FastAPI"]
    assert updated.notes == "Interesting role"
    assert updated.status == "reviewed"


def test_update_job_raises_when_not_found(db):
    service = JobService(db)

    with pytest.raises(ValueError, match="Job not found"):
        service.update_job(
            999,
            JobUpdate(title="Backend Developer"),
        )


def test_list_jobs_returns_jobs(db):
    raw_job_1 = create_raw_job(db, raw_text="Python Developer")
    raw_job_2 = create_raw_job(db, raw_text="Data Engineer")

    service = JobService(db)

    job_1 = service.create_job_from_raw(raw_job_1.id)
    job_2 = service.create_job_from_raw(raw_job_2.id)

    jobs = service.list_jobs()

    job_ids = {job.id for job in jobs}

    assert job_1.id in job_ids
    assert job_2.id in job_ids