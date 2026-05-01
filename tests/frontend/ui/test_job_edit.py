import runpy

import pytest

from tests.frontend.conftest import StopException


def test_job_edit_no_selected_job(fake_streamlit, page_path):
    with pytest.raises(StopException):
        runpy.run_path(page_path("job_edit.py"))

    assert fake_streamlit.messages["warning"]


def test_job_edit_save_updates_job(fake_streamlit, page_path, monkeypatch):
    from ui import api_client

    fake_streamlit.session_state.selected_structured_job_id = 7
    fake_streamlit.clicked_buttons.add("💾 Save")

    fake_streamlit.text_inputs = {
        "Title": "Senior Python Backend Developer",
        "Company": "Acme",
        "Location": "Remote",
        "Skills (comma separated)": "Python, FastAPI, PostgreSQL",
    }
    fake_streamlit.text_areas = {
        "Description": "Updated description",
    }

    captured = {}

    def fake_get_job(job_id):
        assert job_id == 7
        return {
            "id": 7,
            "title": "",
            "company": "",
            "location": "",
            "description": "",
            "skills": [],
        }

    def fake_update_job(job_id, data):
        captured["job_id"] = job_id
        captured["data"] = data
        return {"id": job_id, **data}

    monkeypatch.setattr(api_client, "get_job", fake_get_job)
    monkeypatch.setattr(api_client, "update_job", fake_update_job)

    runpy.run_path(page_path("job_edit.py"))

    assert captured["job_id"] == 7
    assert captured["data"]["title"] == "Senior Python Backend Developer"
    assert captured["data"]["company"] == "Acme"
    assert captured["data"]["location"] == "Remote"
    assert captured["data"]["description"] == "Updated description"
    assert captured["data"]["skills"] == ["Python", "FastAPI", "PostgreSQL"]
    assert fake_streamlit.messages["success"]