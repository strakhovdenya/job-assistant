import os
import subprocess
import sys

from openai import OpenAI


MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def get_diff() -> str:
    try:
        return subprocess.check_output(
            ["git", "diff", "origin/main...HEAD"],
            text=True,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as exc:
        print("Failed to get git diff:")
        print(exc.output)
        sys.exit(1)


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set")
        sys.exit(1)

    diff = get_diff()

    if not diff.strip():
        print("No diff found.")
        return

    client = OpenAI()

    prompt = f"""
Ты senior Python code reviewer.

Проверь этот git diff. Ищи:
- баги
- edge cases
- проблемы с типизацией
- проблемы с тестируемостью
- security issues
- лишнюю сложность

Формат ответа:
## Summary
Кратко.

## Problems
Список конкретных проблем.

## Suggested fixes
Конкретные исправления.

Diff:
```diff
{diff}
"""

    try:
        response = client.responses.create(
            model=MODEL,
            input=prompt,
        )
    except Exception as exc:
        print(f"OpenAI API request failed: {exc}")
        sys.exit(1)

    print(response.output_text)

if __name__ == "__main__":
    main()