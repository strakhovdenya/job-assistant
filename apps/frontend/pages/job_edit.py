import streamlit as st

from ui.api_client import ApiClientError, get_job, update_job

st.set_page_config(page_title="Edit Job", page_icon="✏️", layout="wide")

STATUS_OPTIONS = ["new", "reviewed", "applied", "interviewing", "rejected", "archived"]
LANGUAGE_OPTIONS = ["", "en", "de", "ru", "other"]
SENIORITY_OPTIONS = ["", "junior", "middle", "senior", "lead", "other"]
REMOTE_TYPE_OPTIONS = ["", "remote", "hybrid", "onsite"]
EMPLOYMENT_TYPE_OPTIONS = ["", "full_time", "part_time", "contract", "freelance", "internship"]


def get_selected_job_id() -> int:
    job_id = st.session_state.get("selected_structured_job_id")

    try:
        return int(job_id)
    except (TypeError, ValueError):
        st.warning("No valid job selected. Open a job from Jobs first.")
        st.stop()


def get_option_index(options: list[str], value: str | None) -> int:
    if value in options:
        return options.index(value)
    return 0


def init_skills_state(job_id: int, skills: list[str] | None) -> None:
    skills_key = f"job_edit_skills_{job_id}"

    if skills_key not in st.session_state:
        st.session_state[skills_key] = list(skills or [])


def add_skill(job_id: int) -> None:
    skills_key = f"job_edit_skills_{job_id}"
    input_key = f"job_edit_new_skill_{job_id}"

    skill = st.session_state.get(input_key, "").strip()
    if not skill:
        return

    existing = st.session_state.get(skills_key, [])
    existing_normalized = {item.lower() for item in existing}

    if skill.lower() not in existing_normalized:
        st.session_state[skills_key] = [*existing, skill]

    st.session_state[input_key] = ""


def remove_skill(job_id: int, skill: str) -> None:
    skills_key = f"job_edit_skills_{job_id}"
    st.session_state[skills_key] = [
        item for item in st.session_state.get(skills_key, []) if item != skill
    ]


def render_skills_editor(job_id: int) -> list[str]:
    skills_key = f"job_edit_skills_{job_id}"
    input_key = f"job_edit_new_skill_{job_id}"

    st.subheader("Skills")

    col_input, col_button = st.columns([4, 1])

    with col_input:
        st.text_input(
            "New skill",
            key=input_key,
            placeholder="Python, FastAPI, PostgreSQL...",
        )

    with col_button:
        st.write("")
        st.write("")
        st.button(
            "Add",
            key=f"add_skill_{job_id}",
            on_click=add_skill,
            args=(job_id,),
            use_container_width=True,
        )

    skills = st.session_state.get(skills_key, [])

    if not skills:
        st.info("No skills added yet.")
        return []

    for skill in skills:
        skill_col, remove_col = st.columns([4, 1])

        with skill_col:
            st.write(f"• {skill}")

        with remove_col:
            st.button(
                "Remove",
                key=f"remove_skill_{job_id}_{skill}",
                on_click=remove_skill,
                args=(job_id, skill),
                use_container_width=True,
            )

    return list(st.session_state.get(skills_key, []))


job_id = get_selected_job_id()

st.title(f"✏️ Edit Job #{job_id}")

if st.button("⬅ Back to Jobs"):
    st.switch_page("pages/jobs.py")

try:
    job = get_job(job_id)
except ApiClientError as exc:
    st.error(str(exc))
    st.stop()

init_skills_state(job_id, job.get("skills"))

with st.form("job_edit_form"):
    st.subheader("Main info")

    title = st.text_input("Title", value=job.get("title") or "")
    company = st.text_input("Company", value=job.get("company") or "")
    location = st.text_input("Location", value=job.get("location") or "")

    col1, col2 = st.columns(2)

    with col1:
        language = st.selectbox(
            "Language",
            options=LANGUAGE_OPTIONS,
            index=get_option_index(LANGUAGE_OPTIONS, job.get("language")),
        )

        seniority = st.selectbox(
            "Seniority",
            options=SENIORITY_OPTIONS,
            index=get_option_index(SENIORITY_OPTIONS, job.get("seniority")),
        )

        remote_type = st.selectbox(
            "Remote type",
            options=REMOTE_TYPE_OPTIONS,
            index=get_option_index(REMOTE_TYPE_OPTIONS, job.get("remote_type")),
        )

    with col2:
        employment_type = st.selectbox(
            "Employment type",
            options=EMPLOYMENT_TYPE_OPTIONS,
            index=get_option_index(
                EMPLOYMENT_TYPE_OPTIONS,
                job.get("employment_type"),
            ),
        )

        status = st.selectbox(
            "Status",
            options=STATUS_OPTIONS,
            index=get_option_index(STATUS_OPTIONS, job.get("status") or "new"),
        )

    description = st.text_area(
        "Description",
        value=job.get("description") or "",
        height=300,
    )

    notes = st.text_area(
        "Notes",
        value=job.get("notes") or "",
        height=160,
    )

    submitted = st.form_submit_button("💾 Save", type="primary")

skills = render_skills_editor(job_id)

if submitted:
    try:
        updated_job = update_job(
            job_id,
            {
                "title": title.strip() or None,
                "company": company.strip() or None,
                "location": location.strip() or None,
                "language": language or None,
                "seniority": seniority or None,
                "remote_type": remote_type or None,
                "employment_type": employment_type or None,
                "status": status,
                "description": description.strip() or None,
                "notes": notes.strip() or None,
                "skills": skills,
                "skills_source": "manual",
            },
        )
        st.success(f"Job #{updated_job['id']} saved.")
    except ApiClientError as exc:
        st.error(str(exc))