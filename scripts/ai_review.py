import os
import subprocess
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_diff() -> str:
    return subprocess.check_output(
        ["git", "diff", "origin/main...HEAD"],
        text=True,
    )


diff = get_diff()

if not diff.strip():
    print("No changes to review.")
    raise SystemExit(0)

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

response = client.responses.create(
model="gpt-4.1-mini",
input=prompt,
)

print(response.output_text)