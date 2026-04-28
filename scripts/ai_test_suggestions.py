from pathlib import Path
import os
import subprocess
import sys

from openai import OpenAI


BASE_BRANCH = os.getenv("BASE_BRANCH", "origin/main")

MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

INPUT_PRICE_PER_1M = 0.40
OUTPUT_PRICE_PER_1M = 1.60

MAX_DIFF_CHARS = 12_000
MAX_FILE_CHARS = 6_000
MAX_TEST_FILES = 50
MAX_OUTPUT_TOKENS = 400


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)


def truncate_text(text: str, max_chars: int, label: str) -> str:
    if len(text) <= max_chars:
        return text

    return text[:max_chars] + f"\n\n[{label} TRUNCATED]"


def read_file(path: str) -> str:
    file_path = Path(path)

    if not file_path.exists() or not file_path.is_file():
        return ""

    return file_path.read_text(encoding="utf-8", errors="ignore")


def collect_changed_python_files() -> list[str]:
    changed_files = run(
        ["git", "diff", "--name-only", f"{BASE_BRANCH}...HEAD"]
    ).splitlines()

    return [
        file
        for file in changed_files
        if file.endswith(".py") and not file.startswith("tests/")
    ]


def collect_existing_test_file_names() -> str:
    tests_dir = Path("tests")

    if not tests_dir.exists():
        return "No tests directory found."

    test_files = sorted(tests_dir.rglob("test_*.py"))[:MAX_TEST_FILES]

    if not test_files:
        return "No test files found."

    return "\n".join(str(path) for path in test_files)



def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("OPENAI_API_KEY is not set")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    diff = run(["git", "diff", f"{BASE_BRANCH}...HEAD"])

    if not diff.strip():
        print("No changes found.")
        return

    diff = truncate_text(diff, MAX_DIFF_CHARS, "DIFF")

    changed_python_files = collect_changed_python_files()
    if not changed_python_files:
        print("No Python changes found.")
        return

    changed_code_parts = []

    for file in changed_python_files:
        content = read_file(file)

        if content:
            content = truncate_text(content, MAX_FILE_CHARS, "FILE")
            changed_code_parts.append(
                f"\n===== CHANGED FILE: {file} =====\n{content}\n"
            )

    changed_code_text = (
        "\n".join(changed_code_parts)
        if changed_code_parts
        else "No changed Python files found."
    )

    existing_test_files_text = collect_existing_test_file_names()

    prompt = f"""
Ты senior Python QA engineer.

Твоя задача — определить, каких тест-кейсов НЕ хватает в pull request.

Важно:
- Не пиши полный код pytest-тестов.
- Не генерируй test-файлы.
- Дай только короткие рекомендации по тест-кейсам.
- Не придумывай тесты только по diff.
- Сравни изменения с доступным контекстом.
- Если кейс уже очевидно покрыт существующим test-файлом по названию, не предлагай его.
- Не выдумывай несуществующие функции, классы или API.
- Если тестов достаточно, так и напиши.

Проанализируй:
1. Git diff
2. Короткий контекст изменённых Python-файлов
3. Список уже существующих test-файлов

Верни ответ строго в таком формате:

## Test coverage risk

Low / Medium / High

## Existing coverage

Что, судя по названиям test-файлов и diff, уже может быть покрыто.

## Missing test cases

Короткий список недостающих тест-кейсов.
Для каждого:
- proposed test name
- what it should verify
- why it matters

## Notes

Короткие замечания, если есть.

===== GIT DIFF =====
{diff}

===== CHANGED PYTHON FILES =====
{changed_code_text}

===== EXISTING TEST FILES =====
{existing_test_files_text}
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt,
        max_output_tokens=MAX_OUTPUT_TOKENS,
    )

    usage = response.usage

    input_tokens = usage.input_tokens if usage else 0
    output_tokens = usage.output_tokens if usage else 0
    total_tokens = input_tokens + output_tokens

    estimated_cost = (
        input_tokens / 1_000_000 * INPUT_PRICE_PER_1M
        + output_tokens / 1_000_000 * OUTPUT_PRICE_PER_1M
    )

    print(response.output_text)

    print("\n---")
    print("## Token usage")
    print(f"Model: `{MODEL}`")
    print(f"Input tokens: `{input_tokens}`")
    print(f"Output tokens: `{output_tokens}`")
    print(f"Total tokens: `{total_tokens}`")
    print(f"Estimated cost: `${estimated_cost:.6f}`")


if __name__ == "__main__":
    main()

