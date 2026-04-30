import os
from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.models.job import Job
from app.models.raw_job import RawJob
from app.repositories.job_repository import (
    create_from_raw,
    get_by_id,
    list_jobs,
    update,
)
from app.schemas.job import JobUpdate


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://job_assistant:job_assistant@localhost:5432/job_assistant",
)


@pytest.fixture
def db() -> Generator[Session, None, None]:
    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(bind=engine)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def raw_job(db: Session) -> RawJob:
    raw = RawJob(
        raw_text="Python Backend Developer vacancy",
        source="test",
        content_hash="test_hash_1",
        processing_status="raw",
    )

    db.add(raw)
    db.commit()
    db.refresh(raw)

    return raw


def test_create_from_raw_sets_status_new(db: Session, raw_job: RawJob) -> None:
    job = create_from_raw(db, raw_job)

    assert job.status == "new"


def test_create_from_raw_adds_job_to_db(db: Session, raw_job: RawJob) -> None:
    job = create_from_raw(db, raw_job)

    saved_job = db.query(Job).filter(Job.id == job.id).first()

    assert saved_job is not None
    assert saved_job.raw_job_id == raw_job.id
    assert saved_job.description == raw_job.raw_text


def test_create_from_raw_does_not_update_raw_job_status(
    db: Session,
    raw_job: RawJob,
) -> None:
    create_from_raw(db, raw_job)

    db.refresh(raw_job)

    assert raw_job.processing_status == "raw"


def test_get_by_id_returns_job_if_exists(db: Session, raw_job: RawJob) -> None:
    job = create_from_raw(db, raw_job)

    result = get_by_id(db, job.id)

    assert result is not None
    assert result.id == job.id


def test_get_by_id_returns_none_if_not_found(db: Session) -> None:
    result = get_by_id(db, 999_999)

    assert result is None


def test_update_function_updates_fields_correctly(
    db: Session,
    raw_job: RawJob,
) -> None:
    job = create_from_raw(db, raw_job)

    updated_job = update(
        db,
        job,
        JobUpdate(
            title="Backend Engineer",
            company="Test Company",
            skills=["Python", "FastAPI"],
        ),
    )

    assert updated_job.title == "Backend Engineer"
    assert updated_job.company == "Test Company"
    assert updated_job.skills == ["Python", "FastAPI"]


def test_update_function_does_not_touch_unspecified_fields(
    db: Session,
    raw_job: RawJob,
) -> None:
    job = create_from_raw(db, raw_job)
    job.company = "Original Company"
    db.add(job)
    db.commit()
    db.refresh(job)

    updated_job = update(
        db,
        job,
        JobUpdate(title="Updated Title"),
    )

    assert updated_job.title == "Updated Title"
    assert updated_job.company == "Original Company"


def test_list_jobs_orders_by_created_at_desc(db: Session, raw_job: RawJob) -> None:
    first_job = create_from_raw(db, raw_job)

    second_raw_job = RawJob(
        raw_text="Second vacancy",
        source="test",
        content_hash="test_hash_2",
        processing_status="raw",
    )
    db.add(second_raw_job)
    db.commit()
    db.refresh(second_raw_job)

    second_job = create_from_raw(db, second_raw_job)

    jobs = list_jobs(db)

    assert len(jobs) == 2
    assert jobs[0].created_at >= jobs[1].created_at
    assert {job.id for job in jobs} == {first_job.id, second_job.id}