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

    if settings.ai_provider == "fake":
        return FakeAIClient()

    if settings.ai_provider == "openai_compatible":
        if not settings.ai_api_key:
            raise ValueError("AI_API_KEY is required for openai_compatible provider")

        if not settings.ai_model:
            raise ValueError("AI_MODEL is required for openai_compatible provider")

        return OpenAICompatibleAIClient(
            api_key=settings.ai_api_key,
            model=settings.ai_model,
            base_url=settings.ai_base_url,
            timeout_seconds=settings.ai_timeout_seconds,
        )

    raise ValueError(f"Unsupported AI provider: {settings.ai_provider}")