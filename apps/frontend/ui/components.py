import streamlit as st


def render_raw_job_card(raw_job: dict) -> None:
    with st.container(border=True):
        st.subheader(f"RawJob #{raw_job['id']}")
        st.write(f"**Source:** {raw_job['source']}")
        st.write(f"**Created at:** {raw_job['created_at']}")
        st.write(f"**Content hash:** `{raw_job['content_hash']}`")

        preview = raw_job["raw_text"]
        if len(preview) > 400:
            preview = preview[:400] + "..."

        st.write("**Text preview:**")
        st.write(preview)