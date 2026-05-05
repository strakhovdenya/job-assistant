from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from app.schemas.job_draft import AIExtractionResult
from app.services.ai.ai_client import AIClient, AIClientError


class PipelineError(Exception):
    pass


class PipelineValidationError(PipelineError):
    pass


@dataclass
class PipelineContext:
    raw_text: str
    cleaned_text: str | None = None
    extraction_result: AIExtractionResult | None = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class PipelineStep(ABC):
    @abstractmethod
    def run(self, context: PipelineContext) -> PipelineContext:
        pass


class CleanTextStep(PipelineStep):
    def run(self, context: PipelineContext) -> PipelineContext:
        if context.raw_text is None:
            message = "Raw text is missing"
            context.errors.append(message)
            raise PipelineValidationError(message)

        cleaned_text = context.raw_text.strip()

        if not cleaned_text:
            message = "Raw text is empty"
            context.errors.append(message)
            raise PipelineValidationError(message)

        context.cleaned_text = cleaned_text
        return context


class ExtractStructuredDataStep(PipelineStep):
    def __init__(self, ai_client: AIClient) -> None:
        self.ai_client = ai_client

    def run(self, context: PipelineContext) -> PipelineContext:
        text = context.cleaned_text or context.raw_text

        try:
            context.extraction_result = self.ai_client.extract_job(text)
        except AIClientError as exc:
            context.errors.append(str(exc))
            raise

        return context


class ValidateResultStep(PipelineStep):
    def run(self, context: PipelineContext) -> PipelineContext:
        if context.extraction_result is None:
            message = "AI extraction result is missing"
            context.errors.append(message)
            raise PipelineValidationError(message)

        return context


class JobExtractionPipeline:
    def __init__(self, steps: list[PipelineStep]) -> None:
        self.steps = steps

    def run(self, context: PipelineContext) -> PipelineContext:
        for step in self.steps:
            next_context = step.run(context)

            if not isinstance(next_context, PipelineContext):
                raise PipelineValidationError(
                    f"{step.__class__.__name__} returned invalid pipeline context"
                )

            context = next_context

        return context


def build_job_extraction_pipeline(ai_client: AIClient) -> JobExtractionPipeline:
    return JobExtractionPipeline(
        steps=[
            CleanTextStep(),
            ExtractStructuredDataStep(ai_client),
            ValidateResultStep(),
        ]
    )
