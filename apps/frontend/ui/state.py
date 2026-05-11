import streamlit as st


def init_state() -> None:
    if "selected_job_id" not in st.session_state:
        st.session_state.selected_job_id = None

    if "selected_structured_job_id" not in st.session_state:
        st.session_state.selected_structured_job_id = None

    if "selected_raw_job_id" not in st.session_state:
        st.session_state.selected_raw_job_id = None

    if "selected_job_draft_id" not in st.session_state:
        st.session_state.selected_job_draft_id = None


def set_selected_job_id(job_id: int) -> None:
    st.session_state.selected_job_id = job_id


def get_selected_job_id() -> int | None:
    return st.session_state.get("selected_job_id")


def set_selected_structured_job_id(job_id: int) -> None:
    st.session_state.selected_structured_job_id = job_id


def get_selected_structured_job_id() -> int | None:
    return st.session_state.get("selected_structured_job_id")


def set_selected_raw_job_id(raw_job_id: int) -> None:
    st.session_state.selected_raw_job_id = raw_job_id


def get_selected_raw_job_id() -> int | None:
    return st.session_state.get("selected_raw_job_id")


def set_selected_job_draft_id(job_draft_id: int) -> None:
    st.session_state.selected_job_draft_id = job_draft_id


def get_selected_job_draft_id() -> int | None:
    return st.session_state.get("selected_job_draft_id")


def clear_selected_job_draft_id() -> None:
    st.session_state.selected_job_draft_id = None