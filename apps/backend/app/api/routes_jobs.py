from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.job import JobResponse, JobUpdate
from app.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])


def get_job_service(db: Session = Depends(get_db)) -> JobService:
    return JobService(db)


@router.post(
    "/from-raw/{raw_job_id}",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job_from_raw(
    raw_job_id: int,
    service: JobService = Depends(get_job_service),
) -> JobResponse:
    try:
        job = service.create_job_from_raw(raw_job_id)
        return JobResponse.model_validate(job)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[JobResponse])
def list_jobs(
    service: JobService = Depends(get_job_service),
) -> list[JobResponse]:
    jobs = service.list_jobs()
    return [JobResponse.model_validate(job) for job in jobs]


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    service: JobService = Depends(get_job_service),
) -> JobResponse:
    try:
        job = service.get_job(job_id)
        return JobResponse.model_validate(job)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with id={job_id} not found",
        )


@router.patch("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    payload: JobUpdate,
    service: JobService = Depends(get_job_service),
) -> JobResponse:
    try:
        job = service.update_job(job_id, payload)
        return JobResponse.model_validate(job)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with id={job_id} not found",
        )