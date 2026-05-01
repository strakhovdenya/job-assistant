import streamlit as st

from ui.api_client import ApiClientError, create_job_from_raw, get_raw_job
from ui.state import get_selected_job_id, init_state

st.set_page_config(page_title="Raw Job Detail", page_icon="🔎", layout="wide")
init_state()

st.title("🔎 Raw Job Detail")

default_job_id = get_selected_job_id() or 1

job_id = st.number_input(
    "RawJob ID",
    min_value=1,
    value=int(default_job_id),
    step=1,
)

try:
    raw_job = get_raw_job(int(job_id))

    st.subheader(f"RawJob #{raw_job['id']}")
    st.write(f"**Source:** {raw_job['source']}")
    st.write(f"**Processing status:** {raw_job.get('processing_status', '-')}")
    st.write(f"**Created at:** {raw_job['created_at']}")
    st.write(f"**Content hash:** `{raw_job['content_hash']}`")

    st.write("**Raw text:**")
    st.text_area(
        "Raw text content",
        value=raw_job["raw_text"],
        height=400,
        disabled=True,
    )

    st.divider()

    if st.button("🚀 Create Job", type="primary"):
        try:
            job = create_job_from_raw(int(job_id))
            st.success(f"Job created: #{job['id']}")
            st.session_state.selected_structured_job_id = job["id"]
            st.switch_page("pages/job_edit.py")
        except ApiClientError as exc:
            st.error(str(exc))

except ApiClientError as exc:
    st.error(str(exc))