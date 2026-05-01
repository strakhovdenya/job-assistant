import streamlit as st

from ui.api_client import ApiClientError, list_jobs

st.set_page_config(page_title="Jobs", page_icon="📋", layout="wide")

st.title("📋 Jobs")

try:
    jobs = list_jobs()
except ApiClientError as exc:
    st.error(str(exc))
    st.stop()

if not jobs:
    st.info("No jobs yet.")
    st.stop()

st.caption(f"Total jobs: {len(jobs)}")

for job in jobs:
    with st.container(border=True):
        col1, col2 = st.columns([5, 1])

        with col1:
            st.subheader(job.get("title") or f"Job #{job['id']}")
            st.write(f"**Company:** {job.get('company') or '-'}")
            st.write(f"**Location:** {job.get('location') or '-'}")
            st.write(f"**Status:** {job.get('status') or '-'}")
            st.write(f"**Created at:** {job.get('created_at') or '-'}")

            skills = job.get("skills") or []
            if skills:
                st.write("**Skills:** " + ", ".join(skills))

        with col2:
            if st.button("Open", key=f"open_job_{job['id']}"):
                st.session_state.selected_structured_job_id = job["id"]
                st.switch_page("pages/job_edit.py")