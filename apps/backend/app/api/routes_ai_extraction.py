from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.job_draft import JobDraftResponse
from app.services.ai.ai_extraction_pipeline import AIExtractionPipeline

router = APIRouter(prefix="/raw-jobs", tags=["AI Extraction"])


@router.post("/{raw_job_id}/extract", response_model=JobDraftResponse)
def extract_job(
    raw_job_id: int,
    db: Session = Depends(get_db),
) -> JobDraftResponse:
    pipeline = AIExtractionPipeline(db=db)

    try:
        draft = pipeline.run(raw_job_id)
        return draft

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))