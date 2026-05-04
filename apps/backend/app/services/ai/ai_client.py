import json
from abc import ABC, abstractmethod
from typing import Any

from pydantic import ValidationError

from app.schemas.job_draft import AIExtractionResult


class AIClientError(Exception):
    """Base AI client error."""


class AIClientInvalidResponseError(AIClientError):
    """Raised when AI provider returns invalid or unexpected response."""


class AIClientTimeoutError(AIClientError):
    """Raised when AI provider request times out."""


class AIClientProviderError(AIClientError):
    """Raised when AI provider fails."""


class AIClient(ABC):
    @abstractmethod
    def extract_job(self, raw_text: str) -> AIExtractionResult:
        """Extract structured job data from raw job text."""


class FakeAIClient(AIClient):
    def extract_job(self, raw_text: str) -> AIExtractionResult:
        return AIExtractionResult(
            title="Backend Developer",
            company="Example Company",
            location=None,
            language="en",
            seniority="middle",
            remote_type="remote",
            employment_type="full_time",
            skills=["python", "fastapi", "postgresql"],
            description="Backend developer role extracted from raw job text.",
            confidence=0.8,
            warnings=[],
        )


class OpenAICompatibleAIClient(AIClient):
    def __init__(
        self,
        *,
        api_key: str,
        model: str,
        base_url: str | None = None,
        timeout_seconds: int = 30,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.timeout_seconds = timeout_seconds

    def extract_job(self, raw_text: str) -> AIExtractionResult:
        try:
            response_text = self._call_provider(raw_text)
            return self._parse_response(response_text)
        except AIClientError:
            raise
        except TimeoutError as exc:
            raise AIClientTimeoutError("AI provider request timed out") from exc

    def _call_provider(self, raw_text: str) -> str:
        """
        Real provider call will be implemented after prompt design.

        For now this class defines the production-facing contract,
        while tests and pipeline can use FakeAIClient.
        """
        raise AIClientProviderError("OpenAI-compatible client is not implemented yet")

    def _parse_response(self, response_text: str) -> AIExtractionResult:
        try:
            data: dict[str, Any] = json.loads(response_text)
        except json.JSONDecodeError as exc:
            raise AIClientInvalidResponseError("AI provider returned invalid JSON") from exc

        try:
            return AIExtractionResult.model_validate(data)
        except ValidationError as exc:
            raise AIClientInvalidResponseError("AI provider returned invalid schema") from exc