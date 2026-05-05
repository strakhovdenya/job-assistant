import pytest

from app.schemas.job_draft import AIExtractionResult
from app.services.ai.ai_client import (
    AIClientInvalidResponseError,
    FakeAIClient,
    OpenAICompatibleAIClient,
)


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


def test_openai_compatible_client_parses_valid_json_response():
    client = StubOpenAICompatibleAIClient(
        """
        {
          "title": "Python Developer",
          "company": "Acme",
          "language": "en",
          "seniority": "middle",
          "remote_type": "remote",
          "employment_type": "full_time",
          "skills": [" Python ", "FastAPI", "fastapi"],
          "confidence": 0.75,
          "warnings": []
        }
        """
    )

    result = client.extract_job("raw text")

    assert result.title == "Python Developer"
    assert result.company == "Acme"
    assert result.skills == ["python", "fastapi"]
    assert result.confidence == 0.75


def test_openai_compatible_client_rejects_invalid_json_response():
    client = StubOpenAICompatibleAIClient("not json")

    with pytest.raises(AIClientInvalidResponseError):
        client.extract_job("raw text")


def test_openai_compatible_client_rejects_invalid_schema_response():
    client = StubOpenAICompatibleAIClient(
        """
        {
          "confidence": 1.5
        }
        """
    )

    with pytest.raises(AIClientInvalidResponseError):
        client.extract_job("raw text")

def test_openai_compatible_client_extract_job_calls_prompt_loader(monkeypatch):
    from app.services.ai import ai_client as ai_client_module
    from app.services.ai.ai_client import OpenAICompatibleAIClient

    called = {}

    def fake_build_job_extraction_messages(raw_text: str):
        called["raw_text"] = raw_text
        return [{"role": "user", "content": "test prompt"}]

    class TestClient(OpenAICompatibleAIClient):
        def _call_provider(self, messages):
            return """
            {
              "title": "Backend Developer",
              "company": "Example Company",
              "location": null,
              "language": "en",
              "seniority": "middle",
              "remote_type": "remote",
              "employment_type": "full_time",
              "skills": ["python"],
              "description": "Test description",
              "confidence": 0.8,
              "warnings": []
            }
            """

    monkeypatch.setattr(
        ai_client_module,
        "build_job_extraction_messages",
        fake_build_job_extraction_messages,
    )

    client = TestClient(api_key="test", model="test-model")

    result = client.extract_job("raw job text")

    assert called["raw_text"] == "raw job text"
    assert result.title == "Backend Developer"

def test_openai_compatible_client_extract_job_wraps_timeout():
    from app.services.ai.ai_client import AIClientTimeoutError, OpenAICompatibleAIClient

    class TimeoutClient(OpenAICompatibleAIClient):
        def _call_provider(self, messages):
            raise TimeoutError

    client = TimeoutClient(api_key="test", model="test-model")

    with pytest.raises(AIClientTimeoutError):
        client.extract_job("raw job text")

def test_openai_compatible_client_extract_job_keeps_provider_error():
    from app.services.ai.ai_client import AIClientProviderError, OpenAICompatibleAIClient

    class ProviderErrorClient(OpenAICompatibleAIClient):
        def _call_provider(self, messages):
            raise AIClientProviderError("provider failed")

    client = ProviderErrorClient(api_key="test", model="test-model")

    with pytest.raises(AIClientProviderError):
        client.extract_job("raw job text")

