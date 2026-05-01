import streamlit as st

from ui.api_client import ApiClientError, get_job, update_job

st.set_page_config(page_title="Edit Job", page_icon="✏️", layout="wide")

job_id = st.session_state.get("selected_structured_job_id")

if not job_id:
    st.warning("No job selected. Open a job from Jobs List first.")
    st.stop()

job_id = int(job_id)

st.title(f"✏️ Edit Job #{job_id}")

if st.button("⬅ Back to Jobs"):
    st.switch_page("pages/jobs.py")

try:
    job = get_job(job_id)

    title = st.text_input("Title", value=job.get("title") or "")
    company = st.text_input("Company", value=job.get("company") or "")
    location = st.text_input("Location", value=job.get("location") or "")

    description = st.text_area(
        "Description",
        value=job.get("description") or "",
        height=300,
    )

    skills_input = st.text_input(
        "Skills (comma separated)",
        value=", ".join(job.get("skills") or []),
    )

    if st.button("💾 Save", type="primary"):
        updated_job = update_job(
            job_id,
            {
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "skills": [s.strip() for s in skills_input.split(",") if s.strip()],
            },
        )
        st.success(f"Job #{updated_job['id']} saved.")

except ApiClientError as exc:
    st.error(str(exc))