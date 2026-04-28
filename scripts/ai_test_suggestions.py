from pathlib import Path
import os
import subprocess

from openai import OpenAI


BASE_BRANCH = os.getenv("BASE_BRANCH", "origin/main")
MAX_TEST_FILES = 30


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)


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


def collect_existing_tests() -> list[Path]:
    tests_dir = Path("tests")

    if not tests_dir.exists():
        return []

    return sorted(tests_dir.rglob("test_*.py"))[:MAX_TEST_FILES]


def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing")

    client = OpenAI(api_key=api_key)

    diff = run(["git", "diff", f"{BASE_BRANCH}...HEAD"])

    if not diff.strip():
        print("No changes found.")
        return

    changed_python_files = collect_changed_python_files()

    changed_code_parts = []

    for file in changed_python_files:
        content = read_file(file)

        if content:
            changed_code_parts.append(
                f"\n===== CHANGED FILE: {file} =====\n{content}\n"
            )

    existing_test_parts = []

    for test_file in collect_existing_tests():
        content = test_file.read_text(encoding="utf-8", errors="ignore")

        existing_test_parts.append(
            f"\n===== EXISTING TEST FILE: {test_file} =====\n{content}\n"
        )

    changed_code_text = (
        "\n".join(changed_code_parts)
        if changed_code_parts
        else "No changed Python files found."
    )

    existing_tests_text = (
        "\n".join(existing_test_parts)
        if existing_test_parts
        else "No existing tests found."
    )

    prompt = f"""
Ты senior Python QA engineer.

Твоя задача — определить, каких тестов НЕ хватает в pull request.

Важно:
- Не придумывай тесты только по diff.
- Сравни изменения с уже существующими тестами.
- Если кейс уже покрыт существующими тестами, не предлагай его.
- Не выдумывай несуществующие функции, классы или API.
- Предлагай только pytest-тесты.
- Если тестов достаточно, так и напиши.

Проанализируй:
1. Git diff
2. Полный код изменённых Python-файлов
3. Уже существующие тесты из папки tests/

Верни ответ строго в таком формате:

## Test coverage risk

Low / Medium / High

## Existing coverage

Что уже покрыто существующими тестами.

## Missing coverage

Какие кейсы не покрыты.

## Suggested pytest tests

Только новые тесты, которые действительно стоит добавить.

## Notes

Короткие замечания, если есть.

===== GIT DIFF =====
{diff}

===== CHANGED PYTHON FILES =====
{changed_code_text}

===== EXISTING TESTS =====
{existing_tests_text}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    print(response.output_text)


if __name__ == "__main__":
    main()