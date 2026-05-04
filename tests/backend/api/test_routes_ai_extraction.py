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

    response = client.post(f"/raw-jobs/{raw_job.id}/extract")

    assert response.status_code == 200

    data = response.json()

    assert data["raw_job_id"] == raw_job.id
    assert "title" in data
    assert "skills" in data


def test_extract_job_not_found(client):
    response = client.post("/raw-jobs/999/extract")

    assert response.status_code == 400
    assert "RawJob not found" in response.text


def test_extract_job_already_exists(client, db):
    raw_job = create_raw_job(db)

    response1 = client.post(f"/raw-jobs/{raw_job.id}/extract")
    assert response1.status_code == 200

    response2 = client.post(f"/raw-jobs/{raw_job.id}/extract")
    assert response2.status_code == 400
    assert "already exists" in response2.text