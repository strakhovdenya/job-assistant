from sqlalchemy.orm import Session

from app.models.job_draft import JobDraft
from app.models.raw_job import RawJob


def create_raw_job(db: Session) -> RawJob:
    raw_job = RawJob(
        raw_text="Python developer needed",
        source="test",
        content_hash="hash-job-draft-api",
    )

    db.add(raw_job)
    db.commit()
    db.refresh(raw_job)

    return raw_job


def create_job_draft(db: Session) -> JobDraft:
    raw_job = create_raw_job(db)

    draft = JobDraft(
        raw_job_id=raw_job.id,
        title="Backend Developer",
        company="Test Company",
        location="Berlin",
        language="en",
        seniority="middle",
        remote_type="remote",
        employment_type="full_time",
        skills=["python", "fastapi"],
        description="Build APIs",
        extraction_status="draft",
    )

    db.add(draft)
    db.commit()
    db.refresh(draft)

    return draft


def test_get_job_draft(client, db: Session):
    draft = create_job_draft(db)

    response = client.get(f"/job-drafts/{draft.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == draft.id
    assert data["raw_job_id"] == draft.raw_job_id
    assert data["title"] == "Backend Developer"


def test_update_job_draft(client, db: Session):
    draft = create_job_draft(db)

    response = client.patch(
        f"/job-drafts/{draft.id}",
        json={
            "title": "Senior Backend Developer",
            "skills": ["python", "fastapi", "postgresql"],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == draft.id
    assert data["title"] == "Senior Backend Developer"
    assert data["skills"] == ["python", "fastapi", "postgresql"]


def test_accept_job_draft(client, db: Session):
    draft = create_job_draft(db)

    response = client.post(f"/job-drafts/{draft.id}/accept")

    assert response.status_code == 200

    data = response.json()

    assert data["raw_job_id"] == draft.raw_job_id
    assert data["title"] == draft.title
    assert data["company"] == draft.company
    assert data["skills"] == draft.skills


def test_accept_job_draft_twice_returns_409(client, db: Session):
    draft = create_job_draft(db)

    first_response = client.post(f"/job-drafts/{draft.id}/accept")
    assert first_response.status_code == 200

    second_response = client.post(f"/job-drafts/{draft.id}/accept")

    assert second_response.status_code == 409
    assert "already accepted" in second_response.text

def test_update_job_draft_invalid_payload(client, db: Session):
    draft = create_job_draft(db)

    response = client.patch(
        f"/job-drafts/{draft.id}",
        json={
            "seniority": "super-senior",
        },
    )

    assert response.status_code == 422
