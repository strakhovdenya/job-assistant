import streamlit as st

from ui.api_client import (
    ApiClientError,
    accept_job_draft,
    get_job_draft,
    update_job_draft,
)
from ui.state import (
    get_selected_job_draft_id,
    init_state,
)

st.set_page_config(page_title="AI Draft Editor", page_icon="🤖", layout="wide")
init_state()

st.title("🤖 AI Draft Editor")

draft_id = get_selected_job_draft_id()

if draft_id is None:
    st.info("No AI draft selected.")
    st.stop()

try:
    draft = get_job_draft(draft_id)

    st.subheader(f"Draft #{draft['id']}")

    title = st.text_input("Title", value=draft.get("title") or "")
    company = st.text_input("Company", value=draft.get("company") or "")
    location = st.text_input("Location", value=draft.get("location") or "")

    language = st.text_input("Language", value=draft.get("language") or "")
    seniority = st.text_input("Seniority", value=draft.get("seniority") or "")
    remote_type = st.text_input("Remote type", value=draft.get("remote_type") or "")
    employment_type = st.text_input(
        "Employment type",
        value=draft.get("employment_type") or "",
    )

    description = st.text_area("Description", value=draft.get("description") or "")

    skills_str = st.text_input(
        "Skills (comma separated)",
        value=", ".join(draft.get("skills") or []),
    )

    skills = [skill.strip() for skill in skills_str.split(",") if skill.strip()]

    col_save, col_accept = st.columns(2)

    with col_save:
        if st.button("💾 Save Draft"):
            update_job_draft(
                draft_id,
                {
                    "title": title,
                    "company": company,
                    "location": location,
                    "language": language,
                    "seniority": seniority,
                    "remote_type": remote_type,
                    "employment_type": employment_type,
                    "description": description,
                    "skills": skills,
                },
            )

            st.success("Draft saved.")
            st.rerun()

    with col_accept:
        if st.button("🚀 Save as Job"):
            job = accept_job_draft(draft_id)
            st.session_state.selected_structured_job_id = job["id"]
            st.success(f"Job created: {job['id']}")
            st.switch_page("pages/job_edit.py")

    st.divider()

    st.write("**AI confidence:**", draft.get("ai_confidence"))
    st.write("**AI warnings:**", draft.get("ai_warnings") or [])

except ApiClientError as exc:
    st.error(str(exc))