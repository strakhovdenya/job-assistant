import pytest
from pydantic import ValidationError

from app.schemas.job_draft import AIExtractionResult


def test_ai_extraction_result_accepts_missing_fields_as_none():
    result = AIExtractionResult.model_validate({})

    assert result.title is None
    assert result.company is None
    assert result.location is None
    assert result.language is None
    assert result.seniority is None
    assert result.remote_type is None
    assert result.employment_type is None
    assert result.skills == []
    assert result.description is None
    assert result.confidence is None
    assert result.warnings == []


def test_ai_extraction_result_normalizes_skills():
    result = AIExtractionResult.model_validate(
        {
            "skills": [
                " Python ",
                "FastAPI",
                "fastapi",
                "",
                "  Docker  ",
            ]
        }
    )

    assert result.skills == ["python", "fastapi", "docker"]


def test_ai_extraction_result_ignores_extra_fields():
    result = AIExtractionResult.model_validate(
        {
            "title": "Backend Developer",
            "unexpected_field": "should be ignored",
        }
    )

    assert result.title == "Backend Developer"
    assert not hasattr(result, "unexpected_field")


def test_ai_extraction_result_rejects_invalid_confidence():
    with pytest.raises(ValidationError):
        AIExtractionResult.model_validate({"confidence": 1.5})


def test_ai_extraction_result_rejects_invalid_enum_like_fields():
    with pytest.raises(ValidationError):
        AIExtractionResult.model_validate(
            {
                "language": "spanish",
                "seniority": "principal",
                "remote_type": "moon_base",
                "employment_type": "forever",
            }
        )