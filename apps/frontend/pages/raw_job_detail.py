import streamlit as st

from ui.api_client import (
    ApiClientError,
    generate_ai_draft,
    get_raw_job,
)
from ui.state import (
    get_selected_raw_job_id,
    init_state,
    set_selected_job_draft_id,
)

st.set_page_config(page_title="Raw Job Detail", page_icon="🔎", layout="wide")
init_state()

st.title("🔎 Raw Job Detail")

default_raw_job_id = get_selected_raw_job_id() or 1

raw_job_id = st.number_input(
    "RawJob ID",
    min_value=1,
    value=int(default_raw_job_id),
    step=1,
)

try:
    raw_job = get_raw_job(int(raw_job_id))

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

    button_label = "🤖 Generate AI Draft"

    if raw_job.get("processing_status") in {
        "ai_drafted",
        "structured",
        "failed",
    }:
        button_label = "🔁 Regenerate AI Draft"

    if st.button(button_label, type="primary"):
        try:
            with st.spinner("Generating AI draft..."):
                draft = generate_ai_draft(int(raw_job_id))

            set_selected_job_draft_id(draft["id"])

            st.success(f"Draft generated: #{draft['id']}")
            st.switch_page("pages/job_draft_edit.py")

        except ApiClientError as exc:
            st.error(str(exc))

except ApiClientError as exc:
    st.error(str(exc))