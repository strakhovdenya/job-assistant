import runpy

from ui.api_client import ApiClientError


def test_job_detail_create_job_button_success(fake_streamlit, page_path, monkeypatch):
    from ui import api_client

    fake_streamlit.number_inputs = {
        "RawJob ID": 2,
    }
    fake_streamlit.clicked_buttons.add("🚀 Create Job")

    def fake_get_raw_job(raw_job_id):
        return {
            "id": raw_job_id,
            "source": "manual",
            "processing_status": "raw",
            "created_at": "2025-01-01",
            "content_hash": "abc",
            "raw_text": "Raw job text",
        }

    def fake_create_job_from_raw(raw_job_id):
        assert raw_job_id == 2
        return {"id": 10, "raw_job_id": raw_job_id}

    monkeypatch.setattr(api_client, "get_raw_job", fake_get_raw_job)
    monkeypatch.setattr(api_client, "create_job_from_raw", fake_create_job_from_raw)

    runpy.run_path(page_path("job_detail.py"))

    assert fake_streamlit.session_state.selected_structured_job_id == 10
    assert fake_streamlit.switched_page == "pages/job_edit.py"
    assert fake_streamlit.messages["success"]


def test_job_detail_create_job_button_api_error(fake_streamlit, page_path, monkeypatch):
    from ui import api_client

    fake_streamlit.number_inputs = {
        "RawJob ID": 2,
    }
    fake_streamlit.clicked_buttons.add("🚀 Create Job")

    def fake_get_raw_job(raw_job_id):
        return {
            "id": raw_job_id,
            "source": "manual",
            "processing_status": "raw",
            "created_at": "2025-01-01",
            "content_hash": "abc",
            "raw_text": "Raw job text",
        }

    def fake_create_job_from_raw(raw_job_id):
        raise ApiClientError("API failed")

    monkeypatch.setattr(api_client, "get_raw_job", fake_get_raw_job)
    monkeypatch.setattr(api_client, "create_job_from_raw", fake_create_job_from_raw)

    runpy.run_path(page_path("job_detail.py"))

    assert fake_streamlit.messages["error"]
    assert fake_streamlit.switched_page is None