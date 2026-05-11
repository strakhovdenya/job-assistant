import runpy


def test_raw_jobs_list_filters_and_open_button(fake_streamlit, page_path, monkeypatch):
    from ui import api_client

    def fake_list_raw_jobs(limit, offset, sort_by, sort_order):
        assert limit == 20
        assert offset == 0
        assert sort_by == "created_at"
        assert sort_order == "desc"

        return {
            "items": [
                {
                    "id": 2,
                    "source": "manual",
                    "created_at": "2025-01-01",
                    "content_hash": "abc",
                    "raw_text": "Raw job text",
                }
            ],
            "total": 1,
        }

    monkeypatch.setattr(api_client, "list_raw_jobs", fake_list_raw_jobs)

    fake_streamlit.clicked_buttons.add("open_raw_2")

    runpy.run_path(page_path("raw_jobs.py"))

    assert fake_streamlit.session_state.selected_raw_job_id == 2
    assert fake_streamlit.switched_page == "pages/raw_job_detail.py"

def test_raw_jobs_generate_ai_draft_button(fake_streamlit, page_path, monkeypatch):
    from ui import api_client

    def fake_list_raw_jobs(limit, offset, sort_by, sort_order):
        return {
            "items": [
                {
                    "id": 2,
                    "source": "manual",
                    "created_at": "2025-01-01",
                    "content_hash": "abc",
                    "raw_text": "Raw job text",
                }
            ],
            "total": 1,
        }

    def fake_generate_ai_draft(raw_job_id):
        assert raw_job_id == 2
        return {
            "id": 10,
            "raw_job_id": 2,
            "title": "Python Developer",
            "company": "Acme",
        }

    monkeypatch.setattr(api_client, "list_raw_jobs", fake_list_raw_jobs)
    monkeypatch.setattr(api_client, "generate_ai_draft", fake_generate_ai_draft)

    fake_streamlit.clicked_buttons.add("generate_ai_draft_2")

    runpy.run_path(page_path("raw_jobs.py"))

    assert fake_streamlit.session_state.selected_job_draft_id == 10
    assert fake_streamlit.switched_page == "pages/job_draft_edit.py"
    assert fake_streamlit.messages["success"]