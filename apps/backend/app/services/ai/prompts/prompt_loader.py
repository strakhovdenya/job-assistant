from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from jinja2 import StrictUndefined, Template, UndefinedError


PROMPTS_DIR = Path(__file__).parent


class PromptNotFoundError(ValueError):
    pass


class PromptTemplateError(ValueError):
    pass


@lru_cache
def load_prompt(prompt_name: str, version: int) -> dict[str, Any]:
    prompt_path = PROMPTS_DIR / f"{prompt_name}.v{version}.yaml"

    if not prompt_path.exists():
        raise PromptNotFoundError(
            f"Prompt '{prompt_name}' version {version} not found"
        )

    with prompt_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise PromptTemplateError("Prompt file must contain a YAML object")

    required_fields = {"id", "version", "system", "user_template"}
    missing_fields = required_fields - data.keys()

    if missing_fields:
        raise PromptTemplateError(
            f"Prompt is missing required fields: {sorted(missing_fields)}"
        )

    return data


def build_prompt_messages(
    *,
    prompt_name: str,
    version: int,
    variables: dict[str, str],
) -> list[dict[str, str]]:
    prompt = load_prompt(prompt_name, version)

    try:
        system_prompt = Template(
            prompt["system"],
            undefined=StrictUndefined,
        ).render(**variables)

        user_prompt = Template(
            prompt["user_template"],
            undefined=StrictUndefined,
        ).render(**variables)

    except UndefinedError as exc:
        raise PromptTemplateError("Prompt contains unresolved template variables") from exc

    return [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": user_prompt.strip()},
    ]

def build_job_extraction_messages(raw_text: str) -> list[dict[str, str]]:
    return build_prompt_messages(
        prompt_name="job_extraction",
        version=1,
        variables={
            "raw_text": raw_text,
        },
    )
