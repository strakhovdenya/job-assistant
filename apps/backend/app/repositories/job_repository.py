from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.raw_job import RawJob
from app.schemas.job import JobUpdate


def create_from_raw(db: Session, raw_job: RawJob) -> Job:
    job = Job(
        raw_job_id=raw_job.id,
        title=None,
        company=None,
        status="draft",
        skills=[],
        skills_source="manual",
        description=raw_job.raw_text,
    )

    raw_job.processing_status = "structured"

    db.add(job)
    db.add(raw_job)
    db.commit()
    db.refresh(job)

    return job


def get_by_id(db: Session, job_id: int) -> Job | None:
    return db.query(Job).filter(Job.id == job_id).first()


def list_jobs(db: Session) -> list[Job]:
    return db.query(Job).order_by(Job.created_at.desc()).all()


def update(db: Session, job: Job, data: JobUpdate) -> Job:
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(job, field, value)

    db.add(job)
    db.commit()
    db.refresh(job)

    return job