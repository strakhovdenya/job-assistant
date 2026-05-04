from app.core.job_statuses import (
    JOB_DRAFT_STATUS_DRAFT,
    JOB_DRAFT_STATUS_FAILED,
    JOB_DRAFT_STATUS_REVIEWED,
    JOB_DRAFT_STATUS_SAVED,
    RAW_JOB_STATUS_AI_DRAFTED,
    RAW_JOB_STATUS_RAW,
    RAW_JOB_STATUS_REVIEWED,
    RAW_JOB_STATUS_STRUCTURED,
)
from app.core.status_validation import (
    is_valid_job_draft_status,
    is_valid_raw_job_processing_status,
)


def test_valid_raw_job_processing_statuses():
    assert is_valid_raw_job_processing_status(RAW_JOB_STATUS_RAW)
    assert is_valid_raw_job_processing_status(RAW_JOB_STATUS_REVIEWED)
    assert is_valid_raw_job_processing_status(RAW_JOB_STATUS_AI_DRAFTED)
    assert is_valid_raw_job_processing_status(RAW_JOB_STATUS_STRUCTURED)


def test_invalid_raw_job_processing_status():
    assert not is_valid_raw_job_processing_status("unknown")


def test_valid_job_draft_statuses():
    assert is_valid_job_draft_status(JOB_DRAFT_STATUS_DRAFT)
    assert is_valid_job_draft_status(JOB_DRAFT_STATUS_FAILED)
    assert is_valid_job_draft_status(JOB_DRAFT_STATUS_REVIEWED)
    assert is_valid_job_draft_status(JOB_DRAFT_STATUS_SAVED)


def test_invalid_job_draft_status():
    assert not is_valid_job_draft_status("unknown")