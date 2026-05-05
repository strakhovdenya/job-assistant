import pytest

from app.schemas.job_draft import AIExtractionResult
from app.services.ai.pipeline import (
    CleanTextStep,
    ExtractStructuredDataStep,
    JobExtractionPipeline,
    PipelineContext,
    ValidateResultStep, PipelineValidationError,
)
from app.services.ai.ai_client import AIClientProviderError


class DummyAIClient:
    def __init__(self) -> None:
        self.received_text = None

    def extract_job(self, raw_text: str) -> AIExtractionResult:
        self.received_text = raw_text
        return AIExtractionResult(
            title="Backend Developer",
            company="Test Company",
            location="Berlin",
            language="en",
            seniority="middle",
            remote_type="remote",
            employment_type="full_time",
            skills=["python"],
            description="Test description",
            confidence=0.9,
            warnings=[],
        )


class RecordingStep:
    def __init__(self, name: str, calls: list[str]) -> None:
        self.name = name
        self.calls = calls

    def run(self, context: PipelineContext) -> PipelineContext:
        self.calls.append(self.name)
        return context


def test_clean_text_step_strips_raw_text():
    context = PipelineContext(raw_text="  Python developer needed  ")

    result = CleanTextStep().run(context)

    assert result.cleaned_text == "Python developer needed"


def test_extract_structured_data_step_uses_cleaned_text():
    ai_client = DummyAIClient()
    context = PipelineContext(
        raw_text="  raw text  ",
        cleaned_text="clean text",
    )

    result = ExtractStructuredDataStep(ai_client).run(context)

    assert ai_client.received_text == "clean text"
    assert result.extraction_result is not None
    assert result.extraction_result.title == "Backend Developer"


def test_extract_structured_data_step_falls_back_to_raw_text():
    ai_client = DummyAIClient()
    context = PipelineContext(raw_text="raw text")

    ExtractStructuredDataStep(ai_client).run(context)

    assert ai_client.received_text == "raw text"


def test_job_extraction_pipeline_runs_steps_in_order():
    calls: list[str] = []

    pipeline = JobExtractionPipeline(
        steps=[
            RecordingStep("first", calls),
            RecordingStep("second", calls),
        ]
    )

    context = PipelineContext(raw_text="test")

    pipeline.run(context)

    assert calls == ["first", "second"]


def test_job_extraction_pipeline_sets_extraction_result():
    ai_client = DummyAIClient()

    pipeline = JobExtractionPipeline(
        steps=[
            CleanTextStep(),
            ExtractStructuredDataStep(ai_client),
        ]
    )

    context = PipelineContext(raw_text="  Python developer needed  ")

    result = pipeline.run(context)

    assert result.cleaned_text == "Python developer needed"
    assert result.extraction_result is not None
    assert result.extraction_result.skills == ["python"]

def test_validate_result_step_passes_when_result_exists():
    context = PipelineContext(
        raw_text="test",
        extraction_result=AIExtractionResult(
            title="Backend Developer",
            company="Test Company",
            location="Berlin",
            language="en",
            seniority="middle",
            remote_type="remote",
            employment_type="full_time",
            skills=["python"],
            description="Test description",
            confidence=0.9,
            warnings=[],
        ),
    )

    result = ValidateResultStep().run(context)

    assert result.extraction_result is not None
    assert result.errors == []


def test_validate_result_step_raises_when_result_missing():
    context = PipelineContext(raw_text="test")

    try:
        ValidateResultStep().run(context)
    except PipelineValidationError as exc:
        assert str(exc) == "AI extraction result is missing"

    assert context.errors == ["AI extraction result is missing"]

def test_clean_text_step_raises_when_raw_text_is_whitespace_only():
    context = PipelineContext(raw_text="   ")

    with pytest.raises(PipelineValidationError):
        CleanTextStep().run(context)

    assert context.errors == ["Raw text is empty"]


def test_extract_structured_data_step_adds_ai_client_error_to_context():
    class FailingAIClient:
        def extract_job(self, raw_text: str):
            raise AIClientProviderError("AI failed")

    context = PipelineContext(raw_text="test")

    with pytest.raises(AIClientProviderError):
        ExtractStructuredDataStep(FailingAIClient()).run(context)

    assert context.errors == ["AI failed"]


def test_validate_result_step_accumulates_errors_in_context():
    context = PipelineContext(raw_text="test")

    with pytest.raises(PipelineValidationError):
        ValidateResultStep().run(context)

    assert context.errors == ["AI extraction result is missing"]

def test_job_extraction_pipeline_raises_when_step_returns_none():
    class BrokenStep:
        def run(self, context: PipelineContext):
            return None

    pipeline = JobExtractionPipeline(steps=[BrokenStep()])
    context = PipelineContext(raw_text="test")

    with pytest.raises(PipelineValidationError):
        pipeline.run(context)

def test_clean_text_step_raises_when_raw_text_is_none():
    context = PipelineContext(raw_text=None)

    with pytest.raises(PipelineValidationError):
        CleanTextStep().run(context)

    assert context.errors == ["Raw text is missing"]


def test_pipeline_raises_when_step_returns_invalid_type():
    class BrokenStep:
        def run(self, context: PipelineContext):
            return "not a context"

    pipeline = JobExtractionPipeline(steps=[BrokenStep()])
    context = PipelineContext(raw_text="test")

    with pytest.raises(PipelineValidationError):
        pipeline.run(context)
