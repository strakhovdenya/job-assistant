from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.job import JobResponse
from app.schemas.job_draft import JobDraftResponse, JobDraftUpdate
from app.services.job_draft_service import JobDraftService
from app.services.errors import ConflictError, NotFoundError

router = APIRouter(prefix="/job-drafts", tags=["job-drafts"])


def get_job_draft_service(db: Session = Depends(get_db)) -> JobDraftService:
    return JobDraftService(db)


@router.get("/{job_draft_id}", response_model=JobDraftResponse)
def get_job_draft(
    job_draft_id: int,
    service: JobDraftService = Depends(get_job_draft_service),
) -> JobDraftResponse:
    try:
        draft = service.get_job_draft(job_draft_id)
        return JobDraftResponse.model_validate(draft)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@router.patch("/{job_draft_id}", response_model=JobDraftResponse)
def update_job_draft(
    job_draft_id: int,
    payload: JobDraftUpdate,
    service: JobDraftService = Depends(get_job_draft_service),
) -> JobDraftResponse:
    try:
        draft = service.update_job_draft(job_draft_id, payload)
        return JobDraftResponse.model_validate(draft)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@router.post("/{job_draft_id}/accept", response_model=JobResponse)
def accept_job_draft(
    job_draft_id: int,
    service: JobDraftService = Depends(get_job_draft_service),
) -> JobResponse:
    try:
        job = service.accept_job_draft(job_draft_id)
        return JobResponse.model_validate(job)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
