import pytest

from app.models.raw_job import RawJob


def create_raw_job(db):
    raw_job = RawJob(
        raw_text="Python developer needed",
        source="test",
        content_hash="hash-endpoint",
    )
    db.add(raw_job)
    db.commit()
    db.refresh(raw_job)
    return raw_job


def test_extract_job_success(client, db):
    raw_job = create_raw_job(db)

    response = client.post(f"/api/v1/raw-jobs/{raw_job.id}/extract")

    assert response.status_code == 200

    data = response.json()

    assert data["raw_job_id"] == raw_job.id
    assert "title" in data
    assert "skills" in data


def test_extract_job_not_found(client):
    response = client.post("/api/v1/raw-jobs/999/extract")

    assert response.status_code == 400
    assert "RawJob not found" in response.text


def test_extract_job_can_create_multiple_drafts(client, db):
    raw_job = create_raw_job(db)

    response1 = client.post(f"/api/v1/raw-jobs/{raw_job.id}/extract")
    assert response1.status_code == 200

    response2 = client.post(f"/api/v1/raw-jobs/{raw_job.id}/extract")
    assert response2.status_code == 200

    draft1 = response1.json()
    draft2 = response2.json()

    assert draft1["raw_job_id"] == raw_job.id
    assert draft2["raw_job_id"] == raw_job.id
    assert draft1["id"] != draft2["id"]