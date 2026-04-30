from pathlib import Path
import os
import re
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
CONTEXT_LINES = int(os.getenv("CONTEXT_LINES", "40"))

PROJECT_PATHS = tuple(
    path.strip().rstrip("/") + "/"
    for path in os.getenv("PROJECT_PATHS", "").split(",")
    if path.strip()
)

HUNK_RE = re.compile(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


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


def is_in_target_project(path: str) -> bool:
    if not PROJECT_PATHS:
        return True

    return path.startswith(PROJECT_PATHS)


def collect_changed_python_files() -> list[str]:
    changed_files = run(
        ["git", "diff", "--name-only", f"{BASE_BRANCH}...HEAD"]
    ).splitlines()

    return [
        file
        for file in changed_files
        if (
            file.endswith(".py")
            and not file.startswith("tests/")
            and is_in_target_project(file)
        )
    ]


def collect_diff_for_files(files: list[str]) -> str:
    if not files:
        return ""

    per_file_budget = max(1000, MAX_DIFF_CHARS // len(files))
    parts = []

    for file in files:
        file_diff = run(
            ["git", "diff", f"{BASE_BRANCH}...HEAD", "--", file]
        )

        if file_diff.strip():
            file_diff = truncate_text(
                file_diff,
                per_file_budget,
                "FILE DIFF",
            )
            parts.append(
                f"\n===== DIFF FOR: {file} =====\n{file_diff}\n"
            )

    return truncate_text("\n".join(parts), MAX_DIFF_CHARS, "DIFF")


def collect_changed_line_ranges(file: str) -> list[tuple[int, int]]:
    file_diff = run(
        [
            "git",
            "diff",
            "--unified=0",
            f"{BASE_BRANCH}...HEAD",
            "--",
            file,
        ]
    )

    ranges = []

    for line in file_diff.splitlines():
        match = HUNK_RE.match(line)

        if not match:
            continue

        start = int(match.group(1))
        length = int(match.group(2) or "1")

        if length == 0:
            continue

        ranges.append((start, start + length - 1))

    return ranges


def expand_ranges(
    ranges: list[tuple[int, int]],
    context_lines: int,
    total_lines: int,
) -> list[tuple[int, int]]:
    return [
        (
            max(1, start - context_lines),
            min(total_lines, end + context_lines),
        )
        for start, end in ranges
    ]


def merge_ranges(
    ranges: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    if not ranges:
        return []

    ranges = sorted(ranges)
    merged = [ranges[0]]

    for start, end in ranges[1:]:
        last_start, last_end = merged[-1]

        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged


def read_changed_context(
    path: str,
    context_lines: int = CONTEXT_LINES,
) -> str:
    content = read_file(path)

    if not content:
        return ""

    lines = content.splitlines()
    changed_ranges = collect_changed_line_ranges(path)

    if not changed_ranges:
        return truncate_text(content, MAX_FILE_CHARS, "FILE")

    expanded_ranges = expand_ranges(
        changed_ranges,
        context_lines=context_lines,
        total_lines=len(lines),
    )

    merged_ranges = merge_ranges(expanded_ranges)

    parts = []

    for start, end in merged_ranges:
        snippet = "\n".join(lines[start - 1:end])

        parts.append(
            f"--- lines {start}-{end} ---\n{snippet}"
        )

    return truncate_text(
        "\n\n".join(parts),
        MAX_FILE_CHARS,
        "FILE CONTEXT",
    )


def collect_existing_test_file_names(
    changed_files: list[str] | None = None,
) -> str:
    tests_dir = Path("tests")

    if not tests_dir.exists():
        return "No tests directory found."

    all_test_files = sorted(tests_dir.rglob("test_*.py"))

    if not all_test_files:
        return "No test files found."

    if not changed_files:
        return "\n".join(str(path) for path in all_test_files[:MAX_TEST_FILES])

    keywords = set()

    if any(f.startswith("apps/backend/") for f in changed_files):
        keywords.update([
            "backend",
            "api",
            "service",
            "db",
            "model",
            "schema",
            "repository",
        ])

    if any(f.startswith("apps/frontend/") for f in changed_files):
        keywords.update([
            "frontend",
            "ui",
            "component",
            "page",
            "view",
            "form",
            "client",
        ])

    if not keywords:
        return "\n".join(str(path) for path in all_test_files[:MAX_TEST_FILES])

    relevant = [
        path
        for path in all_test_files
        if any(keyword in str(path).lower() for keyword in keywords)
    ]

    selected = relevant[:MAX_TEST_FILES]

    if not selected:
        selected = all_test_files[:MAX_TEST_FILES]

    return "\n".join(str(path) for path in selected)


def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("OPENAI_API_KEY is not set")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    changed_python_files = collect_changed_python_files()

    if not changed_python_files:
        print("No Python changes found.")
        return

    diff = collect_diff_for_files(changed_python_files)

    if not diff.strip():
        print("No changes found.")
        return

    changed_code_parts = []

    for file in changed_python_files:
        content = read_changed_context(file)

        if content:
            changed_code_parts.append(
                f"\n===== CHANGED FILE CONTEXT: {file} =====\n{content}\n"
            )

    changed_code_text = (
        "\n".join(changed_code_parts)
        if changed_code_parts
        else "No changed Python file context found."
    )

    existing_test_files_text = collect_existing_test_file_names(
        changed_python_files
    )

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
- Учитывай, что контекст файлов содержит только фрагменты вокруг изменённых строк, а не полный файл.

Проанализируй:
1. Git diff только по релевантным файлам
2. Фрагменты изменённых Python-файлов вокруг изменённых строк
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

===== CHANGED PYTHON FILE CONTEXT =====
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