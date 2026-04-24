import os
from typing import Any

import requests

DEFAULT_API_BASE_URL = "http://localhost:8000/api/v1"
API_BASE_URL = os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL)


class ApiClientError(Exception):
    pass


def _handle_response(response: requests.Response) -> Any:
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        message = f"API request failed: {response.status_code} {response.text}"
        raise ApiClientError(message) from exc

    try:
        return response.json()
    except ValueError as exc:
        raise ApiClientError("API returned invalid JSON") from exc


def get_health() -> dict[str, Any]:
    response = requests.get(f"{API_BASE_URL}/health", timeout=10)
    return _handle_response(response)


def create_raw_job(raw_text: str, source: str) -> dict[str, Any]:
    payload = {
        "raw_text": raw_text,
        "source": source,
    }
    response = requests.post(f"{API_BASE_URL}/jobs/raw", json=payload, timeout=15)
    return _handle_response(response)


def list_raw_jobs(
    limit: int = 20,
    offset: int = 0,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> dict[str, Any]:
    params = {
        "limit": limit,
        "offset": offset,
        "sort_by": sort_by,
        "sort_order": sort_order,
    }
    response = requests.get(f"{API_BASE_URL}/jobs/raw", params=params, timeout=15)
    return _handle_response(response)


def get_raw_job(raw_job_id: int) -> dict[str, Any]:
    response = requests.get(f"{API_BASE_URL}/jobs/raw/{raw_job_id}", timeout=15)
    return _handle_response(response)