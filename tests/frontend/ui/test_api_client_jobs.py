import pytest
import requests

from ui import api_client
from ui.api_client import ApiClientError


class DummyResponse:
    def __init__(self, json_data=None, status_code=200, text="OK"):
        self._json_data = json_data
        self.status_code = status_code
        self.text = text

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError()

    def json(self):
        return self._json_data


def test_create_job_from_raw(monkeypatch):
    def fake_post(url, timeout):
        assert url.endswith("/jobs/from-raw/1")
        return DummyResponse({"id": 10, "raw_job_id": 1})

    monkeypatch.setattr(api_client.requests, "post", fake_post)

    result = api_client.create_job_from_raw(1)

    assert result["id"] == 10
    assert result["raw_job_id"] == 1


def test_list_jobs(monkeypatch):
    def fake_get(url, timeout):
        assert url.endswith("/jobs")
        return DummyResponse([{"id": 1}, {"id": 2}])

    monkeypatch.setattr(api_client.requests, "get", fake_get)

    result = api_client.list_jobs()

    assert len(result) == 2


def test_get_job(monkeypatch):
    def fake_get(url, timeout):
        assert url.endswith("/jobs/5")
        return DummyResponse({"id": 5})

    monkeypatch.setattr(api_client.requests, "get", fake_get)

    result = api_client.get_job(5)

    assert result["id"] == 5


def test_update_job(monkeypatch):
    payload = {"title": "Python Developer"}

    def fake_patch(url, json, timeout):
        assert url.endswith("/jobs/5")
        assert json == payload
        return DummyResponse({"id": 5, "title": "Python Developer"})

    monkeypatch.setattr(api_client.requests, "patch", fake_patch)

    result = api_client.update_job(5, payload)

    assert result["title"] == "Python Developer"


def test_handle_response_raises_api_client_error():
    response = DummyResponse(status_code=500, text="Internal Server Error")

    with pytest.raises(ApiClientError):
        api_client._handle_response(response)

def test_create_raw_job(monkeypatch):
    def fake_post(url, json, timeout):
        assert url.endswith("/jobs/raw")
        assert json == {
            "raw_text": "Python developer job",
            "source": "manual",
        }
        return DummyResponse(
            {
                "id": 1,
                "raw_text": "Python developer job",
                "source": "manual",
            }
        )

    monkeypatch.setattr(api_client.requests, "post", fake_post)

    result = api_client.create_raw_job(
        raw_text="Python developer job",
        source="manual",
    )

    assert result["id"] == 1
    assert result["raw_text"] == "Python developer job"
    assert result["source"] == "manual"


def test_list_raw_jobs(monkeypatch):
    def fake_get(url, params, timeout):
        assert url.endswith("/jobs/raw")
        assert params == {
            "limit": 20,
            "offset": 0,
            "sort_by": "created_at",
            "sort_order": "desc",
        }
        return DummyResponse(
            {
                "items": [{"id": 1}, {"id": 2}],
                "total": 2,
            }
        )

    monkeypatch.setattr(api_client.requests, "get", fake_get)

    result = api_client.list_raw_jobs(
        limit=20,
        offset=0,
        sort_by="created_at",
        sort_order="desc",
    )

    assert result["total"] == 2
    assert len(result["items"]) == 2


def test_get_raw_job(monkeypatch):
    def fake_get(url, timeout):
        assert url.endswith("/jobs/raw/5")
        return DummyResponse(
            {
                "id": 5,
                "raw_text": "Raw job text",
                "source": "manual",
            }
        )

    monkeypatch.setattr(api_client.requests, "get", fake_get)

    result = api_client.get_raw_job(5)

    assert result["id"] == 5
    assert result["raw_text"] == "Raw job text"


def test_generate_ai_draft(monkeypatch):
    def fake_post(url, timeout):
        assert url.endswith("/raw-jobs/5/extract")
        return DummyResponse(
            {
                "id": 10,
                "raw_job_id": 5,
                "title": "Python Developer",
            }
        )

    monkeypatch.setattr(api_client.requests, "post", fake_post)

    result = api_client.generate_ai_draft(5)

    assert result["id"] == 10
    assert result["raw_job_id"] == 5
    assert result["title"] == "Python Developer"


def test_get_job_draft(monkeypatch):
    def fake_get(url, timeout):
        assert url.endswith("/job-drafts/10")
        return DummyResponse(
            {
                "id": 10,
                "raw_job_id": 5,
                "title": "Python Developer",
            }
        )

    monkeypatch.setattr(api_client.requests, "get", fake_get)

    result = api_client.get_job_draft(10)

    assert result["id"] == 10
    assert result["raw_job_id"] == 5


def test_update_job_draft(monkeypatch):
    payload = {
        "title": "Senior Python Developer",
        "company": "Acme",
    }

    def fake_patch(url, json, timeout):
        assert url.endswith("/job-drafts/10")
        assert json == payload
        return DummyResponse({"id": 10, **payload})

    monkeypatch.setattr(api_client.requests, "patch", fake_patch)

    result = api_client.update_job_draft(10, payload)

    assert result["id"] == 10
    assert result["title"] == "Senior Python Developer"
    assert result["company"] == "Acme"


def test_accept_job_draft(monkeypatch):
    def fake_post(url, timeout):
        assert url.endswith("/job-drafts/10/accept")
        return DummyResponse(
            {
                "id": 99,
                "title": "Python Developer",
                "company": "Acme",
            }
        )

    monkeypatch.setattr(api_client.requests, "post", fake_post)

    result = api_client.accept_job_draft(10)

    assert result["id"] == 99
    assert result["title"] == "Python Developer"
    assert result["company"] == "Acme"

