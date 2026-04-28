from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

import scripts.ai_review as ai_review
import scripts.ai_test_suggestions as ai_test_suggestions


def fake_response(text: str):
    return SimpleNamespace(
        output_text=text,
        usage=SimpleNamespace(input_tokens=100, output_tokens=50),
    )


def test_ai_review_generate_valid_output(monkeypatch, capsys):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    client = Mock()
    client.responses.create.return_value = fake_response(
        """
## Risk

Low

## Must fix

No blocking issues found.

## Nice to have

- Add tests.

## GPT follow-up prompt

Review edge cases.
"""
    )

    with patch("scripts.ai_review.get_diff", return_value="diff --git a/a.py b/a.py"), \
         patch("scripts.ai_review.OpenAI", return_value=client):
        ai_review.main()

    captured = capsys.readouterr()

    assert "## Risk" in captured.out
    assert "## Must fix" in captured.out
    assert "## Nice to have" in captured.out
    assert "## GPT follow-up prompt" in captured.out
    assert "## Token usage" in captured.out


def test_ai_review_handles_no_diff(monkeypatch, capsys):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    with patch("scripts.ai_review.get_diff", return_value=""):
        ai_review.main()

    captured = capsys.readouterr()

    assert "No diff found." in captured.out


def test_ai_test_suggestions_generates_recommendations(monkeypatch, capsys):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    client = Mock()
    client.responses.create.return_value = fake_response(
        """
## Test coverage risk

Medium

## Existing coverage

No obvious coverage.

## Missing test cases

- proposed test name: test_example
- what it should verify: expected behavior
- why it matters: prevents regressions

## Notes

None.
"""
    )

    with patch("scripts.ai_test_suggestions.run") as run_mock, \
         patch("scripts.ai_test_suggestions.read_file", return_value="print('hello')"), \
         patch("scripts.ai_test_suggestions.collect_existing_test_file_names", return_value="No test files found."), \
         patch("scripts.ai_test_suggestions.OpenAI", return_value=client):
        run_mock.side_effect = [
            "diff --git a/app/example.py b/app/example.py",
            "app/example.py\n",
        ]

        ai_test_suggestions.main()

    captured = capsys.readouterr()

    assert "## Test coverage risk" in captured.out
    assert "## Missing test cases" in captured.out
    assert "proposed test name" in captured.out
    assert "## Token usage" in captured.out


def test_ai_test_suggestions_handles_no_python_changes(monkeypatch, capsys):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    with patch("scripts.ai_test_suggestions.run") as run_mock:
        run_mock.side_effect = [
            "diff --git a/README.md b/README.md",
            "README.md\n.github/workflows/ai-review.yml\n",
        ]

        ai_test_suggestions.main()

    captured = capsys.readouterr()

    assert "No Python changes found." in captured.out


def test_ai_test_suggestions_handles_missing_openai_key(monkeypatch, capsys):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(SystemExit) as exc:
        ai_test_suggestions.main()

    captured = capsys.readouterr()

    assert exc.value.code == 1
    assert "OPENAI_API_KEY is not set" in captured.out