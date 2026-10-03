import streamlit as st

from .theme import RISK_BADGE_COLORS


def show_sidebar_brand() -> None:
    with st.container(key="sidebar_brand"):
        st.title("EduRisk", icon=":material/school:")
        st.caption("STUDENT SUCCESS ANALYTICS")


def show_hero(title: str, subtitle: str, description: str) -> None:
    with st.container(key="hero_banner"):
        st.title(title)
        st.subheader(subtitle)
        st.caption(description)


def show_risk_badge(risk_level: str) -> None:
    badge_color = RISK_BADGE_COLORS.get(risk_level, "gray")
    st.badge(risk_level, color=badge_color)


def show_result_card(
    student_name: str,
    score: int,
    attendance: int,
    risk_level: str,
) -> None:
    with st.container(border=True):
        st.subheader(student_name.strip() or "Student risk result")
        score_col, attendance_col = st.columns(2)

        with score_col:
            st.metric("Score", score)

        with attendance_col:
            st.metric("Attendance", f"{attendance}%")

        show_risk_badge(risk_level)