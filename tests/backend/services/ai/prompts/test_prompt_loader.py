import pytest

from app.services.ai.prompts.prompt_loader import (
    PromptNotFoundError,
    PromptTemplateError,
    build_job_extraction_messages,
    build_prompt_messages,
    load_prompt,
)


def test_load_prompt_success():
    prompt = load_prompt("job_extraction", 1)

    assert prompt["id"] == "job_extraction"
    assert prompt["version"] == 1
    assert "system" in prompt
    assert "user_template" in prompt


def test_build_job_extraction_messages_includes_raw_text():
    raw_text = "We are looking for a Python developer in Berlin."

    messages = build_job_extraction_messages(raw_text)

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert raw_text in messages[1]["content"]


def test_build_job_extraction_messages_requires_json_only():
    messages = build_job_extraction_messages("Test job")

    combined = "\n".join(message["content"] for message in messages)

    assert "valid JSON only" in combined
    assert "Do not include markdown" in combined


def test_build_job_extraction_messages_contains_language_rules():
    messages = build_job_extraction_messages("Test job")

    combined = "\n".join(message["content"] for message in messages)

    assert "Russian, German, or English" in combined
    assert '"ru", "de", "en", or "unknown"' in combined
    assert "Translate ONLY human-readable text fields to Russian" in combined
    assert "DO NOT translate skills" in combined


def test_build_prompt_messages_missing_prompt_raises_error():
    with pytest.raises(PromptNotFoundError):
        build_prompt_messages(
            prompt_name="missing_prompt",
            version=1,
            variables={"raw_text": "Test"},
        )


def test_build_prompt_messages_missing_variable_raises_error():
    with pytest.raises(PromptTemplateError):
        build_prompt_messages(
            prompt_name="job_extraction",
            version=1,
            variables={},
        )