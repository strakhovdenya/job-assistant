import runpy

import pytest

from tests.frontend.conftest import StopException


def make_job(**overrides):
    job = {
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
    job.update(overrides)
    return job


def run_job_edit_page(fake_streamlit, page_path, monkeypatch, job=None):
    from ui import api_client

    fake_streamlit.session_state.selected_structured_job_id = 7

    def fake_get_job(job_id):
        assert job_id == 7
        return job or make_job()

    monkeypatch.setattr(api_client, "get_job", fake_get_job)

    return runpy.run_path(page_path("job_edit.py"))


def test_job_edit_no_selected_job(fake_streamlit, page_path):
    with pytest.raises(StopException):
        runpy.run_path(page_path("job_edit.py"))

    assert fake_streamlit.messages["warning"]


def test_get_selected_job_id_handles_invalid_and_calls_stop(
    fake_streamlit,
    page_path,
):
    fake_streamlit.session_state.selected_structured_job_id = "invalid"

    with pytest.raises(StopException):
        runpy.run_path(page_path("job_edit.py"))

    assert fake_streamlit.messages["warning"]


def test_get_option_index(fake_streamlit, page_path, monkeypatch):
    namespace = run_job_edit_page(fake_streamlit, page_path, monkeypatch)

    get_option_index = namespace["get_option_index"]

    assert get_option_index(["", "en", "de"], "de") == 2
    assert get_option_index(["", "en", "de"], "ru") == 0
    assert get_option_index(["", "en", "de"], None) == 0


def test_init_skills_state_initializes_once(fake_streamlit, page_path, monkeypatch):
    namespace = run_job_edit_page(
        fake_streamlit,
        page_path,
        monkeypatch,
        job=make_job(skills=["Python"]),
    )

    init_skills_state = namespace["init_skills_state"]

    assert fake_streamlit.session_state["job_edit_skills_7"] == ["Python"]

    fake_streamlit.session_state["job_edit_skills_7"] = ["FastAPI"]
    init_skills_state(7, ["Python", "PostgreSQL"])

    assert fake_streamlit.session_state["job_edit_skills_7"] == ["FastAPI"]


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
    fake_streamlit.selectbox_values = {
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
        return make_job()

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


def test_form_submit_with_strip_to_none(fake_streamlit, page_path, monkeypatch):
    from ui import api_client

    fake_streamlit.session_state.selected_structured_job_id = 7
    fake_streamlit.clicked_buttons.add("💾 Save")

    fake_streamlit.text_inputs = {
        "Title": "   ",
        "Company": "   ",
        "Location": "   ",
    }
    fake_streamlit.text_areas = {
        "Description": "   ",
        "Notes": "   ",
    }

    captured = {}

    def fake_get_job(job_id):
        assert job_id == 7
        return make_job()

    def fake_update_job(job_id, data):
        captured["data"] = data
        return {"id": job_id, **data}

    monkeypatch.setattr(api_client, "get_job", fake_get_job)
    monkeypatch.setattr(api_client, "update_job", fake_update_job)

    runpy.run_path(page_path("job_edit.py"))

    assert captured["data"]["title"] is None
    assert captured["data"]["company"] is None
    assert captured["data"]["location"] is None
    assert captured["data"]["description"] is None
    assert captured["data"]["notes"] is None


def test_job_edit_add_skill(fake_streamlit, page_path, monkeypatch):
    fake_streamlit.clicked_buttons.add("add_skill_7")
    fake_streamlit.text_inputs = {
        "New skill": "FastAPI",
    }

    run_job_edit_page(
        fake_streamlit,
        page_path,
        monkeypatch,
        job=make_job(skills=["Python"]),
    )

    assert fake_streamlit.session_state["job_edit_skills_7"] == [
        "Python",
        "FastAPI",
    ]


def test_add_skill_deduplicates_case_insensitive(fake_streamlit, page_path, monkeypatch):
    fake_streamlit.clicked_buttons.add("add_skill_7")
    fake_streamlit.text_inputs = {
        "New skill": " python ",
    }

    run_job_edit_page(
        fake_streamlit,
        page_path,
        monkeypatch,
        job=make_job(skills=["Python"]),
    )

    assert fake_streamlit.session_state["job_edit_skills_7"] == ["Python"]


def test_add_skill_clears_input(fake_streamlit, page_path, monkeypatch):
    fake_streamlit.clicked_buttons.add("add_skill_7")
    fake_streamlit.text_inputs = {
        "New skill": "FastAPI",
    }

    run_job_edit_page(
        fake_streamlit,
        page_path,
        monkeypatch,
        job=make_job(skills=["Python"]),
    )

    assert fake_streamlit.session_state["job_edit_new_skill_7"] == ""


def test_job_edit_remove_skill(fake_streamlit, page_path, monkeypatch):
    fake_streamlit.clicked_buttons.add("remove_skill_7_Python")

    run_job_edit_page(
        fake_streamlit,
        page_path,
        monkeypatch,
        job=make_job(skills=["Python", "FastAPI"]),
    )

    assert fake_streamlit.session_state["job_edit_skills_7"] == ["FastAPI"]


def test_remove_skill_removes_proper_skill(fake_streamlit, page_path, monkeypatch):
    fake_streamlit.clicked_buttons.add("remove_skill_7_Python")

    run_job_edit_page(
        fake_streamlit,
        page_path,
        monkeypatch,
        job=make_job(skills=["Python", "FastAPI", "PostgreSQL"]),
    )

    assert fake_streamlit.session_state["job_edit_skills_7"] == [
        "FastAPI",
        "PostgreSQL",
    ]


def test_render_skills_editor_renders_empty_info_and_buttons(
    fake_streamlit,
    page_path,
    monkeypatch,
):
    run_job_edit_page(
        fake_streamlit,
        page_path,
        monkeypatch,
        job=make_job(skills=[]),
    )

    assert "No skills added yet." in fake_streamlit.messages["info"]

    assert {
        "label": "New skill",
        "key": "job_edit_new_skill_7",
    } in fake_streamlit.rendered_text_inputs

    assert {
        "label": "Add",
        "key": "add_skill_7",
    } in fake_streamlit.rendered_buttons