import streamlit as st

from ui.api_client import ApiClientError, get_raw_job
from ui.state import get_selected_job_id, init_state

st.set_page_config(page_title="Job Detail", page_icon="🔎", layout="wide")
init_state()

st.title("🔎 Job Detail")

default_job_id = get_selected_job_id() or 1

job_id = st.number_input(
    "RawJob ID",
    min_value=1,
    value=int(default_job_id),
    step=1,
)

if st.button("Load job", type="primary"):
    try:
        raw_job = get_raw_job(int(job_id))

        st.subheader(f"RawJob #{raw_job['id']}")
        st.write(f"**Source:** {raw_job['source']}")
        st.write(f"**Created at:** {raw_job['created_at']}")
        st.write(f"**Content hash:** `{raw_job['content_hash']}`")

        st.write("**Raw text:**")
        st.text_area(
            "Raw text content",
            value=raw_job["raw_text"],
            height=400,
            disabled=True,
        )

    except ApiClientError as exc:
        st.error(str(exc))