import runpy

import pytest

from tests.frontend.conftest import StopException
from ui.api_client import ApiClientError


def make_draft(**overrides):
    draft = {
        "id": 11,
        "raw_job_id": 2,
        "title": "Python Developer",
        "company": "Acme",
        "location": "Remote",
        "language": "en",
        "seniority": "senior",
        "remote_type": "remote",
        "employment_type": "full_time",
        "description": "Build APIs",
        "skills": ["Python", "FastAPI"],
        "ai_confidence": 0.91,
        "ai_warnings": [],
    }
    draft.update(overrides)
    return draft


def run_job_draft_edit_page(fake_streamlit, page_path, monkeypatch, draft=None):
    from ui import api_client

    fake_streamlit.session_state.selected_job_draft_id = 11

    def fake_get_job_draft(job_draft_id):
        assert job_draft_id == 11
        return draft or make_draft()

    monkeypatch.setattr(api_client, "get_job_draft", fake_get_job_draft)

    return runpy.run_path(page_path("job_draft_edit.py"))


def test_job_draft_edit_no_selected_draft(fake_streamlit, page_path):
    with pytest.raises(StopException):
        runpy.run_path(page_path("job_draft_edit.py"))

    assert "No AI draft selected." in fake_streamlit.messages["info"]


def test_job_draft_edit_renders_draft(fake_streamlit, page_path, monkeypatch):
    run_job_draft_edit_page(fake_streamlit, page_path, monkeypatch)

    assert "Draft #11" in fake_streamlit.messages["write"]
    assert ("**AI confidence:**", 0.91) in fake_streamlit.messages["write"]
    assert ("**AI warnings:**", []) in fake_streamlit.messages["write"]


def test_job_draft_edit_save_draft(fake_streamlit, page_path, monkeypatch):
    from ui import api_client

    fake_streamlit.session_state.selected_job_draft_id = 11
    fake_streamlit.clicked_buttons.add("💾 Save Draft")

    fake_streamlit.text_inputs = {
        "Title": "Senior Python Backend Developer",
        "Company": "Acme GmbH",
        "Location": "Berlin",
        "Language": "en",
        "Seniority": "senior",
        "Remote type": "hybrid",
        "Employment type": "full_time",
        "Skills (comma separated)": "Python, FastAPI, PostgreSQL",
    }

    fake_streamlit.text_areas = {
        "Description": "Updated draft description",
    }

    captured = {}

    def fake_get_job_draft(job_draft_id):
        assert job_draft_id == 11
        return make_draft()

    def fake_update_job_draft(job_draft_id, data):
        captured["job_draft_id"] = job_draft_id
        captured["data"] = data
        return {"id": job_draft_id, **data}

    monkeypatch.setattr(api_client, "get_job_draft", fake_get_job_draft)
    monkeypatch.setattr(api_client, "update_job_draft", fake_update_job_draft)

    runpy.run_path(page_path("job_draft_edit.py"))

    assert captured["job_draft_id"] == 11
    assert captured["data"] == {
        "title": "Senior Python Backend Developer",
        "company": "Acme GmbH",
        "location": "Berlin",
        "language": "en",
        "seniority": "senior",
        "remote_type": "hybrid",
        "employment_type": "full_time",
        "description": "Updated draft description",
        "skills": ["Python", "FastAPI", "PostgreSQL"],
    }
    assert fake_streamlit.messages["success"] == ["Draft saved."]


def test_job_draft_edit_save_as_job(fake_streamlit, page_path, monkeypatch):
    from ui import api_client

    fake_streamlit.session_state.selected_job_draft_id = 11
    fake_streamlit.clicked_buttons.add("🚀 Save as Job")

    def fake_get_job_draft(job_draft_id):
        assert job_draft_id == 11
        return make_draft()

    def fake_accept_job_draft(job_draft_id):
        assert job_draft_id == 11
        return {"id": 99, "job_draft_id": job_draft_id}

    monkeypatch.setattr(api_client, "get_job_draft", fake_get_job_draft)
    monkeypatch.setattr(api_client, "accept_job_draft", fake_accept_job_draft)

    runpy.run_path(page_path("job_draft_edit.py"))

    assert fake_streamlit.session_state.selected_structured_job_id == 99
    assert fake_streamlit.switched_page == "pages/job_edit.py"
    assert fake_streamlit.messages["success"] == ["Job created: 99"]


def test_job_draft_edit_get_draft_api_error(fake_streamlit, page_path, monkeypatch):
    from ui import api_client

    fake_streamlit.session_state.selected_job_draft_id = 11

    def fake_get_job_draft(job_draft_id):
        raise ApiClientError("Cannot load draft")

    monkeypatch.setattr(api_client, "get_job_draft", fake_get_job_draft)

    runpy.run_path(page_path("job_draft_edit.py"))

    assert fake_streamlit.messages["error"] == ["Cannot load draft"]