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