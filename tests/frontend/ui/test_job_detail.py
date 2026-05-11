import runpy

from ui.api_client import ApiClientError


def test_raw_job_detail_generate_ai_draft_success(
    fake_streamlit,
    page_path,
    monkeypatch,
):
    from ui import api_client

    fake_streamlit.number_inputs = {
        "RawJob ID": 2,
    }
    fake_streamlit.clicked_buttons.add("🤖 Generate AI Draft")

    def fake_get_raw_job(raw_job_id):
        assert raw_job_id == 2
        return {
            "id": raw_job_id,
            "source": "manual",
            "processing_status": "raw",
            "created_at": "2025-01-01",
            "content_hash": "abc",
            "raw_text": "Raw job text",
        }

    def fake_generate_ai_draft(raw_job_id):
        assert raw_job_id == 2
        return {
            "id": 10,
            "raw_job_id": raw_job_id,
            "title": "Python Developer",
        }

    monkeypatch.setattr(api_client, "get_raw_job", fake_get_raw_job)
    monkeypatch.setattr(api_client, "generate_ai_draft", fake_generate_ai_draft)

    runpy.run_path(page_path("raw_job_detail.py"))

    assert fake_streamlit.session_state.selected_job_draft_id == 10
    assert fake_streamlit.switched_page == "pages/job_draft_edit.py"
    assert fake_streamlit.messages["success"] == ["Draft generated: #10"]


def test_raw_job_detail_regenerate_ai_draft_success(
    fake_streamlit,
    page_path,
    monkeypatch,
):
    from ui import api_client

    fake_streamlit.number_inputs = {
        "RawJob ID": 2,
    }
    fake_streamlit.clicked_buttons.add("🔁 Regenerate AI Draft")

    def fake_get_raw_job(raw_job_id):
        assert raw_job_id == 2
        return {
            "id": raw_job_id,
            "source": "manual",
            "processing_status": "ai_drafted",
            "created_at": "2025-01-01",
            "content_hash": "abc",
            "raw_text": "Raw job text",
        }

    def fake_generate_ai_draft(raw_job_id):
        assert raw_job_id == 2
        return {
            "id": 11,
            "raw_job_id": raw_job_id,
            "title": "Senior Python Developer",
        }

    monkeypatch.setattr(api_client, "get_raw_job", fake_get_raw_job)
    monkeypatch.setattr(api_client, "generate_ai_draft", fake_generate_ai_draft)

    runpy.run_path(page_path("raw_job_detail.py"))

    assert fake_streamlit.session_state.selected_job_draft_id == 11
    assert fake_streamlit.switched_page == "pages/job_draft_edit.py"
    assert fake_streamlit.messages["success"] == ["Draft generated: #11"]


def test_raw_job_detail_generate_ai_draft_api_error(
    fake_streamlit,
    page_path,
    monkeypatch,
):
    from ui import api_client

    fake_streamlit.number_inputs = {
        "RawJob ID": 2,
    }
    fake_streamlit.clicked_buttons.add("🤖 Generate AI Draft")

    def fake_get_raw_job(raw_job_id):
        assert raw_job_id == 2
        return {
            "id": raw_job_id,
            "source": "manual",
            "processing_status": "raw",
            "created_at": "2025-01-01",
            "content_hash": "abc",
            "raw_text": "Raw job text",
        }

    def fake_generate_ai_draft(raw_job_id):
        raise ApiClientError("API failed")

    monkeypatch.setattr(api_client, "get_raw_job", fake_get_raw_job)
    monkeypatch.setattr(api_client, "generate_ai_draft", fake_generate_ai_draft)

    runpy.run_path(page_path("raw_job_detail.py"))

    assert fake_streamlit.messages["error"] == ["API failed"]
    assert fake_streamlit.switched_page is None