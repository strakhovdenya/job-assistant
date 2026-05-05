from abc import ABC, abstractmethod
from openai import APIConnectionError, APITimeoutError, OpenAI, OpenAIError
import instructor

from pydantic import ValidationError

from app.schemas.job_draft import AIExtractionResult
from app.services.ai.prompts.prompt_loader import build_job_extraction_messages


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

        openai_client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout_seconds,
        )

        self.client = instructor.from_openai(openai_client)

    def extract_job(self, raw_text: str) -> AIExtractionResult:
        try:
            messages = build_job_extraction_messages(raw_text)

            return self.client.chat.completions.create(
                model=self.model,
                response_model=AIExtractionResult,
                messages=messages,
                temperature=0,
            )

        except APITimeoutError as exc:
            raise AIClientTimeoutError("AI provider request timed out") from exc
        except APIConnectionError as exc:
            raise AIClientProviderError("AI provider connection failed") from exc
        except OpenAIError as exc:
            raise AIClientProviderError("AI provider request failed") from exc
        except ValidationError as exc:
            raise AIClientInvalidResponseError("AI provider returned invalid schema") from exc