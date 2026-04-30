from datetime import datetime, timezone
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.api.routes_jobs import get_job_service
from app.main import app


class FakeJob:
    def __init__(
        self,
        *,
        id: int = 1,
        raw_job_id: int = 1,
        title: str | None = None,
        company: str | None = None,
        location: str | None = None,
        language: str | None = None,
        seniority: str | None = None,
        remote_type: str | None = None,
        employment_type: str | None = None,
        status: str = "new",
        skills: list[str] | None = None,
        skills_source: str = "manual",
        description: str | None = "Raw job text",
        notes: str | None = None,
    ) -> None:
        self.id = id
        self.raw_job_id = raw_job_id
        self.title = title
        self.company = company
        self.location = location
        self.language = language
        self.seniority = seniority
        self.remote_type = remote_type
        self.employment_type = employment_type
        self.status = status
        self.skills = skills or []
        self.skills_source = skills_source
        self.description = description
        self.notes = notes
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)


@pytest.fixture
def mock_job_service() -> Mock:
    service = Mock()
    app.dependency_overrides[get_job_service] = lambda: service

    yield service

    app.dependency_overrides.clear()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_create_job_from_raw_endpoint_success(
    client: TestClient,
    mock_job_service: Mock,
) -> None:
    job = FakeJob(id=1, raw_job_id=10)
    mock_job_service.create_job_from_raw.return_value = job

    response = client.post("/api/v1/jobs/from-raw/10")

    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["raw_job_id"] == 10
    assert data["status"] == "new"
    assert data["skills"] == []
    assert data["skills_source"] == "manual"

    mock_job_service.create_job_from_raw.assert_called_once_with(10)


def test_create_job_from_raw_endpoint_raises_400_on_value_error(
    client: TestClient,
    mock_job_service: Mock,
) -> None:
    mock_job_service.create_job_from_raw.side_effect = ValueError("RawJob not found")

    response = client.post("/api/v1/jobs/from-raw/999")

    assert response.status_code == 400
    assert response.json() == {"detail": "RawJob not found"}

    mock_job_service.create_job_from_raw.assert_called_once_with(999)


def test_get_job_endpoint_success(
    client: TestClient,
    mock_job_service: Mock,
) -> None:
    job = FakeJob(
        id=5,
        raw_job_id=2,
        title="Backend Developer",
        company="Acme",
    )
    mock_job_service.get_job.return_value = job

    response = client.get("/api/v1/jobs/5")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 5
    assert data["raw_job_id"] == 2
    assert data["title"] == "Backend Developer"
    assert data["company"] == "Acme"

    mock_job_service.get_job.assert_called_once_with(5)


def test_get_job_endpoint_raises_404_when_job_not_found(
    client: TestClient,
    mock_job_service: Mock,
) -> None:
    mock_job_service.get_job.side_effect = ValueError("Job not found")

    response = client.get("/api/v1/jobs/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Job with id=999 not found"}

    mock_job_service.get_job.assert_called_once_with(999)


def test_update_job_endpoint_success(
    client: TestClient,
    mock_job_service: Mock,
) -> None:
    updated_job = FakeJob(
        id=3,
        raw_job_id=1,
        title="Backend Engineer",
        company="Test Company",
        skills=["Python", "FastAPI"],
        notes="Interesting role",
        status="reviewed",
    )
    mock_job_service.update_job.return_value = updated_job

    payload = {
        "title": "Backend Engineer",
        "company": "Test Company",
        "skills": ["Python", "FastAPI"],
        "notes": "Interesting role",
        "status": "reviewed",
    }

    response = client.patch("/api/v1/jobs/3", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 3
    assert data["title"] == "Backend Engineer"
    assert data["company"] == "Test Company"
    assert data["skills"] == ["Python", "FastAPI"]
    assert data["notes"] == "Interesting role"
    assert data["status"] == "reviewed"

    mock_job_service.update_job.assert_called_once()
    called_job_id, called_payload = mock_job_service.update_job.call_args.args

    assert called_job_id == 3
    assert called_payload.title == "Backend Engineer"
    assert called_payload.company == "Test Company"
    assert called_payload.skills == ["Python", "FastAPI"]
    assert called_payload.notes == "Interesting role"
    assert called_payload.status == "reviewed"


def test_list_jobs_endpoint_success(
    client: TestClient,
    mock_job_service: Mock,
) -> None:
    mock_job_service.list_jobs.return_value = [
        FakeJob(id=1, raw_job_id=1, title="Backend Developer"),
        FakeJob(id=2, raw_job_id=2, title="Data Engineer"),
    ]

    response = client.get("/api/v1/jobs")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["title"] == "Backend Developer"
    assert data[1]["id"] == 2
    assert data[1]["title"] == "Data Engineer"

    mock_job_service.list_jobs.assert_called_once_with()