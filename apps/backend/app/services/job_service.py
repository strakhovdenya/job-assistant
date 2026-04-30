from sqlalchemy.orm import Session

from app.models.job import Job
from app.repositories import job_repository
from app.repositories.raw_job_repository import RawJobRepository
from app.schemas.job import JobUpdate


class JobService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.raw_job_repository = RawJobRepository(db)

    def create_job_from_raw(self, raw_job_id: int) -> Job:
        raw_job = self.raw_job_repository.get_by_id(raw_job_id)

        if raw_job is None:
            raise ValueError("RawJob not found")

        if raw_job.jobs:
            raise ValueError("Job already exists for this RawJob")

        job = job_repository.create_from_raw(self.db, raw_job)

        # 🔥 ключевая бизнес-логика
        raw_job.processing_status = "structured"
        self.db.add(raw_job)
        self.db.commit()

        return job

    def get_job(self, job_id: int) -> Job:
        job = job_repository.get_by_id(self.db, job_id)

        if job is None:
            raise ValueError("Job not found")

        return job

    def list_jobs(self) -> list[Job]:
        return job_repository.list_jobs(self.db)

    def update_job(self, job_id: int, data: JobUpdate) -> Job:
        job = job_repository.get_by_id(self.db, job_id)

        if job is None:
            raise ValueError("Job not found")

        return job_repository.update(self.db, job, data)