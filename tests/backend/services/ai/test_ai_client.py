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