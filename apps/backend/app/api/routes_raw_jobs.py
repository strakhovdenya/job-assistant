from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.raw_job_repository import RawJobRepository
from app.schemas.raw_job import RawJobCreate, RawJobListResponse, RawJobResponse
from app.services.raw_job_service import RawJobService

router = APIRouter(prefix="/jobs/raw", tags=["raw-jobs"])


def get_raw_job_service(db: Session = Depends(get_db)) -> RawJobService:
    repository = RawJobRepository(db)
    return RawJobService(repository)


@router.post("", response_model=RawJobResponse, status_code=status.HTTP_201_CREATED)
def create_raw_job(
    payload: RawJobCreate,
    service: RawJobService = Depends(get_raw_job_service),
) -> RawJobResponse:
    raw_job, created = service.create_raw_job(
        raw_text=payload.raw_text,
        source=payload.source,
    )
    return RawJobResponse.model_validate(raw_job)


@router.get("", response_model=RawJobListResponse)
def list_raw_jobs(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    service: RawJobService = Depends(get_raw_job_service),
) -> RawJobListResponse:
    items, total = service.list_raw_jobs(
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return RawJobListResponse(
        items=[RawJobResponse.model_validate(item) for item in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{raw_job_id}", response_model=RawJobResponse)
def get_raw_job(
    raw_job_id: int,
    service: RawJobService = Depends(get_raw_job_service),
) -> RawJobResponse:
    raw_job = service.get_raw_job(raw_job_id)
    if raw_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RawJob with id={raw_job_id} not found",
        )
    return RawJobResponse.model_validate(raw_job)