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
    }
    fake_streamlit.text_areas = {
        "Description": "Updated description",
        "Notes": "Important notes",
    }
    fake_streamlit.selectbox_values  = {
        "Language": "en",
        "Seniority": "senior",
        "Remote type": "remote",
        "Employment type": "full_time",
        "Status": "new",
    }

    fake_streamlit.session_state["job_edit_skills_7"] = [
        "Python",
        "FastAPI",
        "PostgreSQL",
    ]

    captured = {}

    def fake_get_job(job_id):
        assert job_id == 7
        return {
            "id": 7,
            "title": "",
            "company": "",
            "location": "",
            "language": None,
            "seniority": None,
            "remote_type": None,
            "employment_type": None,
            "status": "new",
            "description": "",
            "notes": "",
            "skills": [],
            "skills_source": "manual",
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
    assert captured["data"]["language"] == "en"
    assert captured["data"]["seniority"] == "senior"
    assert captured["data"]["remote_type"] == "remote"
    assert captured["data"]["employment_type"] == "full_time"
    assert captured["data"]["status"] == "new"
    assert captured["data"]["description"] == "Updated description"
    assert captured["data"]["notes"] == "Important notes"
    assert captured["data"]["skills"] == ["Python", "FastAPI", "PostgreSQL"]
    assert captured["data"]["skills_source"] == "manual"
    assert fake_streamlit.messages["success"]


def test_job_edit_add_skill(fake_streamlit, page_path, monkeypatch):
    from ui import api_client

    fake_streamlit.session_state.selected_structured_job_id = 7
    fake_streamlit.clicked_buttons.add("add_skill_7")
    fake_streamlit.text_inputs = {
        "New skill": "FastAPI",
    }

    def fake_get_job(job_id):
        assert job_id == 7
        return {
            "id": 7,
            "title": "Python Developer",
            "company": "Acme",
            "location": "Remote",
            "language": None,
            "seniority": None,
            "remote_type": None,
            "employment_type": None,
            "status": "new",
            "description": "",
            "notes": "",
            "skills": ["Python"],
            "skills_source": "manual",
        }

    monkeypatch.setattr(api_client, "get_job", fake_get_job)

    runpy.run_path(page_path("job_edit.py"))

    assert fake_streamlit.session_state["job_edit_skills_7"] == [
        "Python",
        "FastAPI",
    ]


def test_job_edit_remove_skill(fake_streamlit, page_path, monkeypatch):
    from ui import api_client

    fake_streamlit.session_state.selected_structured_job_id = 7
    fake_streamlit.clicked_buttons.add("remove_skill_7_Python")

    def fake_get_job(job_id):
        assert job_id == 7
        return {
            "id": 7,
            "title": "Python Developer",
            "company": "Acme",
            "location": "Remote",
            "language": None,
            "seniority": None,
            "remote_type": None,
            "employment_type": None,
            "status": "new",
            "description": "",
            "notes": "",
            "skills": ["Python", "FastAPI"],
            "skills_source": "manual",
        }

    monkeypatch.setattr(api_client, "get_job", fake_get_job)

    runpy.run_path(page_path("job_edit.py"))

    assert fake_streamlit.session_state["job_edit_skills_7"] == ["FastAPI"]