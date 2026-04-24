import streamlit as st

from ui.api_client import ApiClientError, create_raw_job

st.set_page_config(page_title="Add Job", page_icon="➕", layout="wide")

st.title("➕ Add Job")

with st.form("add_job_form"):
    source = st.selectbox(
        "Source",
        options=["manual", "email", "telegram", "linkedin", "other"],
        index=0,
    )
    raw_text = st.text_area(
        "Raw job text",
        height=300,
        placeholder="Вставь сюда текст вакансии...",
    )

    submitted = st.form_submit_button("Create raw job", type="primary")

if submitted:
    if not raw_text.strip():
        st.warning("Raw job text is required.")
    else:
        try:
            result = create_raw_job(raw_text=raw_text, source=source)
            st.success(f"Raw job saved with ID #{result['id']}")
            st.json(result)
        except ApiClientError as exc:
            st.error(str(exc))