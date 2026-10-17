from pathlib import Path

import streamlit as st
import pandas as pd
from styles import load_css
from styles.charts import show_risk_chart, show_score_chart
from styles.components import show_hero, show_result_card, show_sidebar_brand
from styles.tables import show_styled_table

# Step 7: Update the page configuration
st.set_page_config(
    page_title="EduRisk Analytics - Lab 03",
    page_icon="🎓",
    layout="wide"
)
load_css()

def load_student_data():
    student_data_path = Path(__file__).resolve().parent / "data" / "students.csv"
    try:
        return pd.read_csv(student_data_path)
    except FileNotFoundError:
        st.error("data/students.csv was not found. Please place students.csv in the data folder.")
        st.stop()


student_df = load_student_data()

# Step 9: Define a function to determine the risk level based on score and attendance
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"

# Step 10: Add the Risk Level column to the DataFrame
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(row["Score"], row["Attendance"]),
    axis=1
)

# Calculate metrics for the sidebar
total_students = len(student_df)
average_score = student_df["Score"].mean()
average_attendance = student_df["Attendance"].mean()
low_score_students = student_df[student_df["Score"] < 60].shape[0]

# Step 11: Update Sidebar Navigation
page_icons = {
    "Home": "home",
    "Dashboard": "dashboard",
    "Student Data": "table_chart",
    "Risk Checker": "fact_check",
    "About": "info",
}

with st.sidebar:
    show_sidebar_brand()
    selected_page = st.radio(
        "Go to",
        list(page_icons),
        format_func=lambda page: f":material/{page_icons[page]}: {page}",
    )

# Step 12: Update the main content based on the selected page
# Home Page
if selected_page == "Home":
    show_hero(
        "🎓 EduRisk Analytics",
        "Frontend Prototype with CSV Data Loading",
        "Welcome to Lab 03. Explore student performance and academic risk from students.csv.",
    )
    st.success("Lab 03 app is running successfully!")

# Step 13: Create and Start the Dashboard page
# Dashboard Page
elif selected_page == "Dashboard":
    st.title("Dashboard Prototype")
    st.write("Explore student performance using data loaded from students.csv.")

    with st.container(key="dashboard_filters", border=True):
        st.subheader("Filters")
        course_col, risk_col = st.columns(2)

        with course_col:
            selected_course = st.selectbox(
                "Select Course",
                ["All"] + list(student_df["Course"].unique())
            )

        with risk_col:
            selected_risk = st.selectbox(
                "Select Risk Level",
                ["All", "Low Risk", "Medium Risk", "High Risk"]
            )

        attendance_col, score_col = st.columns(2)

        with attendance_col:
            min_attendance = st.slider("Minimum Attendance", 0, 100, 0)

        with score_col:
            min_score = st.slider("Minimum Score", 0, 100, 0)

    # Step 18: Add filtering logic based on user selections
    filtered_df = student_df.copy()

    # Filter based on selected course
    if selected_course != "All":
        filtered_df = filtered_df[filtered_df["Course"] == selected_course]
    # Filter based on selected risk level
    if selected_risk != "All":
        filtered_df = filtered_df[filtered_df["Risk Level"] == selected_risk]

    # Filter based on minimum attendance and score
    filtered_df = filtered_df[
        filtered_df["Attendance"] >= min_attendance
    ]
    # Filter based on minimum score
    filtered_df = filtered_df[
        filtered_df["Score"] >= min_score
    ]

    # Step 19: Add daashboard metrics
    total_students = len(filtered_df)

    # Calculate average score and attendance only if there are students in the filtered DataFrame
    if len(filtered_df) > 0:
        average_score = filtered_df["Score"].mean()
        average_attendance = filtered_df["Attendance"].mean()
    # If no students match the criteria, set metrics to 0
    else:
        average_score = 0
        average_attendance = 0

    # Count the number of high-risk students in the filtered DataFrame
    high_risk_students = filtered_df[
        filtered_df["Risk Level"] == "High Risk"
    ].shape[0]

    st.subheader("Dashboard Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Students", total_students)
    with col2:
        st.metric("Average Score", round(average_score, 2))
    with col3:
        st.metric("Avg. Attendance", f"{round(average_attendance, 2)}%")
    with col4:
        st.metric("High Risk", high_risk_students)

    # Step 20: Add Show or Hide Dataset Checkbox
    show_data = st.checkbox("Show Filtered Dataset", True)
    if show_data:
        st.subheader("Filtered Student Dataset")
        show_styled_table(filtered_df)

        # Step 21: Add Download Button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data",
            data=csv,
            file_name="filtered_student_data.csv",
            mime="text/csv"
        )
    else:
        st.info("Filtered dataset is hidden.")

    # Step 22: Add Student Score Chart
    st.subheader("Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        if len(filtered_df) > 0:
            show_score_chart(filtered_df)
        else:
            st.warning("No data available for score chart.")

    # Step 23: Add Risk Level Count Chart
    with chart_col2:
        if len(filtered_df) > 0:
            show_risk_chart(filtered_df)
        else:
            st.warning("No data available for risk chart.")

# Step 24: Update the Student Data Page
elif selected_page == "Student Data":
    st.title("Student Data")
    st.write("Inspect the dataset loaded from students.csv.")

    st.subheader("Data Inspection")
    st.write("Rows and Columns:", student_df.shape)
    st.write("Column Names:")
    st.write(student_df.columns.tolist())
    st.write("First 5 Rows:")
    show_styled_table(student_df.head())

    total_students = len(student_df)
    average_score = student_df["Score"].mean()
    average_attendance = student_df["Attendance"].mean()
    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric("Avg. Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        st.metric("High Risk Students", high_risk_students)

    st.subheader("Full Student Dataset")
    show_styled_table(student_df)

# Step 25: Create the Risk Checker Page
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")

    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)
        submitted = st.form_submit_button("Check Risk")

    if submitted:
        risk_result = get_risk_level(input_score, input_attendance)
        show_result_card(input_name, input_score, input_attendance, risk_result)

# Step 26: Update the About Page
else:
    st.title("About")
    st.write("This app is part of Lab 03.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Data Loading, Layout, and Frontend Prototype")
    st.info("Ethics Reminder: Risk prediction should support students, not punish them.")
