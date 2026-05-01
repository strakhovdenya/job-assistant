import streamlit as st

from ui.api_client import ApiClientError, list_raw_jobs
from ui.components import render_raw_job_card
from ui.state import init_state, set_selected_job_id

st.set_page_config(page_title="Jobs", page_icon="📋", layout="wide")
init_state()

st.title("📋 Jobs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    limit = st.number_input("Limit", min_value=1, max_value=100, value=20, step=1)

with col2:
    offset = st.number_input("Offset", min_value=0, value=0, step=1)

with col3:
    sort_by = st.selectbox("Sort by", options=["created_at", "id", "source"], index=0)

with col4:
    sort_order = st.selectbox("Sort order", options=["desc", "asc"], index=0)

try:
    response = list_raw_jobs(
        limit=int(limit),
        offset=int(offset),
        sort_by=sort_by,
        sort_order=sort_order,
    )

    st.success(f"Loaded {len(response['items'])} raw jobs. Total: {response['total']}")

    items = response["items"]

    if not items:
        st.info("No raw jobs found.")
        st.stop()

    for item in items:
        render_raw_job_card(item)

        if st.button(f"Open RawJob #{item['id']}", key=f"open_raw_{item['id']}"):
            set_selected_job_id(item["id"])
            st.switch_page("pages/job_detail.py")

except ApiClientError as exc:
    st.error(str(exc))