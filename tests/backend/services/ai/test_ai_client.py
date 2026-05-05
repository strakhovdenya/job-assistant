import pytest

from openai import APIConnectionError, APITimeoutError, OpenAIError
from pydantic import ValidationError

from app.schemas.job_draft import AIExtractionResult
from app.services.ai.ai_client import (
    AIClientInvalidResponseError,
    AIClientProviderError,
    AIClientTimeoutError,
    OpenAICompatibleAIClient,
    FakeAIClient,
)

def make_ai_result() -> AIExtractionResult:
    return AIExtractionResult(
        title="Backend Developer",
        company="Example Company",
        location="Berlin",
        language="en",
        seniority="middle",
        remote_type="remote",
        employment_type="full_time",
        skills=["python", "fastapi"],
        description="Backend role",
        confidence=0.9,
        warnings=[],
    )

class DummyCompletions:
    def __init__(self, result=None, error: Exception | None = None) -> None:
        self.result = result
        self.error = error
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)

        if self.error is not None:
            raise self.error

        return self.result


class DummyChat:
    def __init__(self, completions: DummyCompletions) -> None:
        self.completions = completions


class DummyInstructorClient:
    def __init__(self, completions: DummyCompletions) -> None:
        self.chat = DummyChat(completions)

class StubOpenAICompatibleAIClient(OpenAICompatibleAIClient):
    def __init__(self, response_text: str):
        super().__init__(
            api_key="test-key",
            model="test-model",
            timeout_seconds=30,
        )
        self.response_text = response_text

    def _call_provider(self, raw_text: str) -> str:
        return self.response_text


def test_fake_ai_client_returns_valid_extraction_result():
    client = FakeAIClient()

    result = client.extract_job("Some raw job text")

    assert isinstance(result, AIExtractionResult)
    assert result.title == "Backend Developer"
    assert result.company == "Example Company"
    assert result.skills == ["python", "fastapi", "postgresql"]
    assert result.confidence == 0.8

def test_openai_compatible_client_returns_structured_ai_result(monkeypatch) -> None:
    expected_result = make_ai_result()
    completions = DummyCompletions(result=expected_result)

    client = OpenAICompatibleAIClient(
        api_key="test-key",
        model="test-model",
    )
    client.client = DummyInstructorClient(completions)

    result = client.extract_job("Raw job text")

    assert result == expected_result

    assert len(completions.calls) == 1
    call = completions.calls[0]

    assert call["model"] == "test-model"
    assert call["response_model"] is AIExtractionResult
    assert call["temperature"] == 0
    assert call["messages"][0]["role"] == "system"
    assert call["messages"][1]["role"] == "user"

def test_openai_compatible_client_maps_timeout_error() -> None:
    completions = DummyCompletions(
        error=APITimeoutError(request=None)
    )

    client = OpenAICompatibleAIClient(
        api_key="test-key",
        model="test-model",
    )
    client.client = DummyInstructorClient(completions)

    with pytest.raises(AIClientTimeoutError):
        client.extract_job("Raw job text")

def test_openai_compatible_client_maps_connection_error() -> None:
    completions = DummyCompletions(
        error=APIConnectionError(request=None)
    )

    client = OpenAICompatibleAIClient(
        api_key="test-key",
        model="test-model",
    )
    client.client = DummyInstructorClient(completions)

    with pytest.raises(AIClientProviderError):
        client.extract_job("Raw job text")

def test_openai_compatible_client_maps_openai_error() -> None:
    completions = DummyCompletions(
        error=OpenAIError("provider failed")
    )

    client = OpenAICompatibleAIClient(
        api_key="test-key",
        model="test-model",
    )
    client.client = DummyInstructorClient(completions)

    with pytest.raises(AIClientProviderError):
        client.extract_job("Raw job text")

def test_openai_compatible_client_maps_validation_error() -> None:
    try:
        AIExtractionResult.model_validate({"title": 123})
    except ValidationError as exc:
        validation_error = exc

    completions = DummyCompletions(error=validation_error)

    client = OpenAICompatibleAIClient(
        api_key="test-key",
        model="test-model",
    )
    client.client = DummyInstructorClient(completions)

    with pytest.raises(AIClientInvalidResponseError):
        client.extract_job("Raw job text")

