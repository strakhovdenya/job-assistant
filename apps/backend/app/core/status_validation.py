from app.core.job_statuses import (
    JOB_DRAFT_STATUSES,
    RAW_JOB_PROCESSING_STATUSES,
)


def is_valid_raw_job_processing_status(status: str) -> bool:
    return status in RAW_JOB_PROCESSING_STATUSES


def is_valid_job_draft_status(status: str) -> bool:
    return status in JOB_DRAFT_STATUSES