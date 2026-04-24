import streamlit as st


def init_state() -> None:
    if "selected_job_id" not in st.session_state:
        st.session_state.selected_job_id = None


def set_selected_job_id(job_id: int) -> None:
    st.session_state.selected_job_id = job_id


def get_selected_job_id() -> int | None:
    return st.session_state.get("selected_job_id")