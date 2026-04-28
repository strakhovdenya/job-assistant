import os
import subprocess
import sys

from openai import OpenAI


BASE_BRANCH = os.getenv("BASE_BRANCH", "origin/main")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

INPUT_PRICE_PER_1M = 0.40
OUTPUT_PRICE_PER_1M = 1.60

MAX_DIFF_CHARS = 12_000
MAX_OUTPUT_TOKENS = 500


def run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(
            cmd,
            text=True,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as exc:
        print("Command failed:")
        print(" ".join(cmd))
        print(exc.output)
        sys.exit(1)


def truncate_text(text: str, max_chars: int, label: str) -> str:
    if len(text) <= max_chars:
        return text

    return text[:max_chars] + f"\n\n[{label} TRUNCATED]"


def get_diff() -> str:
    return run(["git", "diff", f"{BASE_BRANCH}...HEAD"])


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set")
        sys.exit(1)

    diff = get_diff()

    if not diff.strip():
        print("No diff found.")
        return

    diff = truncate_text(diff, MAX_DIFF_CHARS, "DIFF")

    client = OpenAI()

    prompt = f"""
Ты senior Python code reviewer.

Сделай компактный review git diff.

Цель:
- найти только реальные проблемы
- не писать длинные объяснения
- не пересказывать diff
- не предлагать стиль ради стиля
- не писать полный patch
- не писать код, если проблема понятна словами

Проверяй:
- баги
- edge cases
- security issues
- проблемы типизации
- проблемы тестируемости
- явные регрессии

Формат ответа строго:

## Risk

Low / Medium / High

## Must fix

Только критичные или реально опасные проблемы.
Максимум 5 пунктов.
Формат пункта:
- file:line — проблема → что сделать

## Nice to have

Некритичные улучшения.
Максимум 5 пунктов.

## GPT follow-up prompt

Короткий промпт, который можно скопировать в GPT-чат для дальнейшего разбора.
Без diff, без длинного контекста.

Если серьёзных проблем нет, напиши:
"No blocking issues found."

===== GIT DIFF =====
{diff}
"""

    try:
        response = client.responses.create(
            model=MODEL,
            input=prompt,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        )
    except Exception as exc:
        print(f"OpenAI API request failed: {exc}")
        sys.exit(1)

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