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

    assert fake_streamlit.session_state.selected_job_id == 2
    assert fake_streamlit.switched_page == "pages/job_detail.py"