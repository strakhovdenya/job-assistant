import logging
import re


from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from app.schemas.job_draft import AIExtractionResult
from app.services.ai.ai_client import AIClient, AIClientError

logger = logging.getLogger(__name__)

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
    detected_language: Optional[str] = None


class PipelineStep(ABC):
    @abstractmethod
    def run(self, context: PipelineContext) -> PipelineContext:
        pass

class DetectLanguageStep(PipelineStep):
    def run(self, context: PipelineContext) -> PipelineContext:
        text = context.cleaned_text or ""

        if not text.strip():
            context.detected_language = "unknown"
            return context

        has_cyrillic = bool(re.search(r"[а-яА-Я]", text))
        has_german_chars = bool(re.search(r"[äöüßÄÖÜ]", text))
        has_latin = bool(re.search(r"[a-zA-Z]", text))

        if has_cyrillic:
            context.detected_language = "ru"
        elif has_german_chars:
            context.detected_language = "de"
        elif has_latin:
            context.detected_language = "en"
        else:
            context.detected_language = "unknown"

        return context

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
    def __init__(self, ai_client: AIClient, max_retries: int = 2) -> None:
        self.ai_client = ai_client
        self.max_retries = max_retries

    def run(self, context: PipelineContext) -> PipelineContext:
        text = context.cleaned_text or context.raw_text
        attempts = self.max_retries + 1

        for attempt in range(1, attempts + 1):
            try:
                context.extraction_result = self.ai_client.extract_job(text)
                return context
            except AIClientError as exc:
                if attempt < attempts:
                    logger.warning(
                        "AI extraction failed, retrying",
                        extra={
                            "attempt": attempt,
                            "max_attempts": attempts,
                            "error": str(exc),
                        },
                    )
                    continue

                message = str(exc)
                context.errors.append(message)

                logger.error(
                    "AI extraction failed after retries",
                    extra={
                        "attempt": attempt,
                        "max_attempts": attempts,
                        "error": message,
                    },
                )

                raise

        return context

class NormalizeFieldsStep(PipelineStep):
    def run(self, context: PipelineContext) -> PipelineContext:
        if context.extraction_result is None:
            return context

        result = context.extraction_result

        result.title = self._normalize_string(result.title)
        result.company = self._normalize_string(result.company)
        result.location = self._normalize_string(result.location)
        result.description = self._normalize_string(result.description)

        result.employment_type = self._normalize_enum(result.employment_type)
        result.remote_type  = self._normalize_enum(result.remote_type)
        result.seniority = self._normalize_enum(result.seniority)
        result.language = self._normalize_enum(result.language)

        result.skills = self._normalize_skills(result.skills)

        return context

    @staticmethod
    def _normalize_string(value: str | None) -> str | None:
        if value is None:
            return None

        cleaned = value.strip()
        return cleaned or None

    @staticmethod
    def _normalize_enum(value: str | None) -> str | None:
        if value is None:
            return None

        cleaned = value.strip().lower()
        cleaned = re.sub(r"[^a-z0-9]+", "_", cleaned)
        cleaned = cleaned.strip("_")

        return cleaned or None

    @staticmethod
    def _normalize_skills(value: list[str] | None) -> list[str]:
        if not value:
            return []

        normalized: list[str] = []

        for skill in value:
            cleaned = skill.strip().lower()

            if cleaned and cleaned not in normalized:
                normalized.append(cleaned)

        return normalized


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
            DetectLanguageStep(),
            ExtractStructuredDataStep(ai_client),
            NormalizeFieldsStep(),
            ValidateResultStep(),
        ]
    )
