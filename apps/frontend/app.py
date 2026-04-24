import streamlit as st

st.set_page_config(
    page_title="AI Job Assistant",
    page_icon="💼",
    layout="wide",
)

st.title("💼 AI Job Assistant")
st.markdown("Минимальный UI для Sprint 1")

st.info(
    "Используй меню слева:\n"
    "- Jobs — список вакансий\n"
    "- Add Job — добавить новую вакансию\n"
    "- Job Detail — посмотреть вакансию по ID"
)