import runpy


def test_jobs_list_navigation(fake_streamlit, page_path, monkeypatch):
    from ui import api_client

    def fake_list_jobs():
        return [
            {
                "id": 2,
                "title": "Python Developer",
                "company": "Acme",
                "location": "Remote",
                "status": "new",
                "created_at": "2025-01-01",
                "skills": ["Python"],
            }
        ]

    monkeypatch.setattr(api_client, "list_jobs", fake_list_jobs)

    fake_streamlit.clicked_buttons.add("open_job_2")

    runpy.run_path(page_path("jobs.py"))

    assert fake_streamlit.session_state.selected_structured_job_id == 2
    assert fake_streamlit.switched_page == "pages/job_edit.py"