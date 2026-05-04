from app.services.ai.ai_client import FakeAIClient, OpenAICompatibleAIClient
from app.services.ai.ai_client_factory import get_ai_client


def test_ai_client_factory_returns_fake_client_by_default():
    client = get_ai_client()

    assert isinstance(client, FakeAIClient)


def test_ai_client_factory_returns_fake_client_when_ai_disabled(monkeypatch):
    monkeypatch.setenv("AI_ENABLED", "false")

    from app.core.config import get_settings

    get_settings.cache_clear()

    client = get_ai_client()

    assert isinstance(client, FakeAIClient)

    get_settings.cache_clear()


def test_ai_client_factory_returns_openai_compatible_client(monkeypatch):
    monkeypatch.setenv("AI_ENABLED", "true")
    monkeypatch.setenv("AI_PROVIDER", "openai_compatible")
    monkeypatch.setenv("AI_API_KEY", "test-key")
    monkeypatch.setenv("AI_MODEL", "test-model")
    monkeypatch.setenv("AI_TIMEOUT_SECONDS", "10")

    from app.core.config import get_settings

    get_settings.cache_clear()

    client = get_ai_client()

    assert isinstance(client, OpenAICompatibleAIClient)
    assert client.api_key == "test-key"
    assert client.model == "test-model"
    assert client.timeout_seconds == 10

    get_settings.cache_clear()