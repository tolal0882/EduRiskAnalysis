from pathlib import Path

import pandas as pd
import streamlit as st

from styles import load_css
from styles.charts import show_risk_chart, show_score_chart
from styles.components import show_feature_pill, show_hero, show_result_card, show_sidebar_brand
from styles.tables import show_styled_table

st.set_page_config(page_title="EduRisk Analytics", page_icon=":material/school:", layout="wide")
load_css()


@st.cache_data
def load_student_data() -> pd.DataFrame:
    """Load the bundled student dataset once per file change."""
    try:
        return pd.read_csv(Path(__file__).resolve().with_name("students.csv"))
    except FileNotFoundError:
        st.error("students.csv was not found. Please place it beside app.py.")
        st.stop()


def get_risk_level(score: int | float, attendance: int | float) -> str:
    if score < 60 or attendance < 60:
        return "High Risk"
    if score < 75 or attendance < 75:
        return "Medium Risk"
    return "Low Risk"


def filtered_students(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Render dashboard controls and return the filtered dataset."""
    with st.container(key="filter_bar", border=True):
        st.subheader("Explore the cohort", icon=":material/tune:")
        course_col, risk_col = st.columns(2)
        with course_col:
            course = st.selectbox("Course", ["All courses", *sorted(dataframe["Course"].unique())])
        with risk_col:
            risk = st.selectbox("Risk level", ["All levels", "Low Risk", "Medium Risk", "High Risk"])
        score_col, attendance_col = st.columns(2)
        with score_col:
            minimum_score = st.slider("Minimum score", 0, 100, 0)
        with attendance_col:
            minimum_attendance = st.slider("Minimum attendance", 0, 100, 0)

    result = dataframe.copy()
    if course != "All courses":
        result = result[result["Course"] == course]
    if risk != "All levels":
        result = result[result["Risk Level"] == risk]
    return result[(result["Score"] >= minimum_score) & (result["Attendance"] >= minimum_attendance)]


student_df = load_student_data().copy()
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(row["Score"], row["Attendance"]), axis=1
)
if "risk_history" not in st.session_state:
    st.session_state.risk_history = []

page_icons = {
    "Home": "home", "Dashboard": "dashboard", "Student Data": "table_chart",
    "Risk Checker": "fact_check", "About": "info",
}
with st.sidebar:
    show_sidebar_brand()
    selected_page = st.radio(
        "Navigate", list(page_icons),
        format_func=lambda page: f":material/{page_icons[page]}: {page}",
        label_visibility="collapsed",
    )
    st.space("large")
    st.caption("Academic support insights • Lab 04")


if selected_page == "Home":
    show_hero(
        "EduRisk Analytics", "A clearer view of student progress",
        "Use course data and thoughtful risk signals to start supportive conversations.",
    )
    first, second, third = st.columns(3)
    with first:
        show_feature_pill(":material/analytics:", "Cohort insights", "View scores, attendance, and risk patterns at a glance.")
    with second:
        show_feature_pill(":material/fact_check:", "Guided checks", "Review a single student's support needs with a simple form.")
    with third:
        show_feature_pill(":material/volunteer_activism:", "Student-first", "Use indicators to offer help, never to label or penalise.")
    st.space("medium")
    total, score, attendance, high_risk = st.columns(4)
    total.metric("Students tracked", len(student_df))
    score.metric("Average score", f"{student_df['Score'].mean():.1f}")
    attendance.metric("Average attendance", f"{student_df['Attendance'].mean():.1f}%")
    high_risk.metric("Needs attention", (student_df["Risk Level"] == "High Risk").sum())
    st.info("Risk indicators are a starting point for support—not a final judgement.", icon=":material/favorite:")

elif selected_page == "Dashboard":
    show_hero(
        "Dashboard", "Cohort performance at a glance",
        "Filter the data to focus on the students and signals that matter right now.",
    )
    filtered_df = filtered_students(student_df)
    total, score, attendance, high_risk = st.columns(4)
    total.metric("Students", len(filtered_df))
    score.metric("Average score", f"{filtered_df['Score'].mean():.1f}" if not filtered_df.empty else "—")
    attendance.metric("Average attendance", f"{filtered_df['Attendance'].mean():.1f}%" if not filtered_df.empty else "—")
    high_risk.metric("High risk", (filtered_df["Risk Level"] == "High Risk").sum())
    if filtered_df.empty:
        st.warning("No students match these filters. Try broadening the criteria.", icon=":material/filter_alt_off:")
    else:
        st.subheader("Student overview", icon=":material/groups:")
        show_styled_table(filtered_df)
        st.download_button(
            "Download filtered data", filtered_df.to_csv(index=False), "edurisk_filtered_students.csv",
            "text/csv", icon=":material/download:",
        )
        st.subheader("Performance patterns", icon=":material/insights:")
        score_chart, risk_chart = st.columns(2)
        with score_chart:
            show_score_chart(filtered_df)
        with risk_chart:
            show_risk_chart(filtered_df)

elif selected_page == "Student Data":
    show_hero(
        "Student data", "Inspect the source data with context",
        "The records below are loaded from students.csv and enriched with the calculated risk level.",
    )
    overview, details = st.columns([1, 2])
    with overview.container(border=True):
        st.subheader("Dataset summary", icon=":material/dataset:")
        st.metric("Records", len(student_df))
        st.metric("Fields", len(student_df.columns))
        st.caption("Columns: " + ", ".join(student_df.columns))
    with details.container(border=True):
        st.subheader("Preview", icon=":material/preview:")
        show_styled_table(student_df.head())
    st.subheader("Full dataset", icon=":material/table:")
    show_styled_table(student_df)

elif selected_page == "Risk Checker":
    show_hero(
        "Risk checker", "Turn a check-in into timely support",
        "Enter a student's current score and attendance to see a supportive risk indicator.",
    )
    with st.form("risk_checker_form", border=True):
        st.subheader("Student check-in", icon=":material/person_search:")
        name_col, score_col, attendance_col = st.columns([2, 1, 1])
        with name_col:
            input_name = st.text_input("Student name", placeholder="e.g. Dara")
        with score_col:
            input_score = st.number_input("Score", min_value=0, max_value=100, value=50)
        with attendance_col:
            input_attendance = st.number_input("Attendance (%)", min_value=0, max_value=100, value=50)
        submitted = st.form_submit_button("Check risk", type="primary", icon=":material/fact_check:")
    if submitted:
        if not input_name.strip():
            st.warning("Enter the student's name before checking risk.", icon=":material/person:")
        else:
            result = {
                "Student Name": input_name.strip(), "Score": input_score,
                "Attendance": input_attendance,
                "Risk Level": get_risk_level(input_score, input_attendance),
            }
            st.session_state.risk_history.append(result)
            show_result_card(
                result["Student Name"], result["Score"], result["Attendance"], result["Risk Level"]
            )
    st.subheader("Recent risk checks", icon=":material/history:")
    if st.session_state.risk_history:
        show_styled_table(pd.DataFrame(st.session_state.risk_history))
        if st.button("Clear history", icon=":material/delete_sweep:"):
            st.session_state.risk_history = []
            st.toast("Risk-check history cleared.", icon=":material/delete:")
            st.rerun()
    else:
        st.caption("Your submitted checks will appear here for this browser session.")
    st.warning(
        "Use risk results as guidance for support, not as a final judgement about a student.",
        icon=":material/volunteer_activism:",
    )

else:
    show_hero(
        "About EduRisk", "A student-support dashboard for Lab 04",
        "Built for the Web App Development for Data Science course.",
    )
    with st.container(border=True):
        st.subheader("Designed with care", icon=":material/auto_awesome:")
        st.markdown("EduRisk Analytics combines CSV-backed data exploration, form validation, and session-based history in a student-first interface.")
        st.info(
            "Academic monitoring should support learning and student success—not label or punish learners.",
            icon=":material/volunteer_activism:",
        )
