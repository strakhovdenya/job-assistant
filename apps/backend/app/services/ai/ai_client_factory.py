from app.core.config import get_settings
from app.services.ai.ai_client import (
    AIClient,
    FakeAIClient,
    OpenAICompatibleAIClient,
)


def get_ai_client() -> AIClient:
    settings = get_settings()

    if not settings.ai_enabled:
        return FakeAIClient()

    provider = settings.ai_provider.lower().strip()

    if provider == "fake":
        return FakeAIClient()

    if provider == "openai":
        if not settings.ai_api_key:
            raise ValueError("AI_API_KEY is required for OpenAI provider")

        return OpenAICompatibleAIClient(
            api_key=settings.ai_api_key,
            model=settings.ai_model,
            base_url=settings.ai_base_url or None,
            timeout_seconds=settings.ai_timeout_seconds,
        )

    raise ValueError(f"Unknown AI provider: {settings.ai_provider}")
