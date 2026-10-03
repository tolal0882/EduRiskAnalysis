import pandas as pd
import streamlit as st
import altair as alt

from .theme import RISK_COLORS, RISK_ORDER, SCORE_COLORS


def show_score_chart(dataframe: pd.DataFrame) -> None:
    st.write("Student Scores")
    chart_data = dataframe[["Student Name", "Score"]].copy()
    chart_data["Band"] = [
        "high" if score < 60 else "medium" if score < 75 else "low"
        for score in chart_data["Score"]
    ]
    chart = (
        alt.Chart(chart_data)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("Student Name:N", title="Student", sort=None),
            y=alt.Y("Score:Q", title="Score", scale=alt.Scale(domain=[0, 100])),
            color=alt.Color(
                "Band:N",
                scale=alt.Scale(
                    domain=["high", "medium", "low"],
                    range=[SCORE_COLORS["high"], SCORE_COLORS["medium"], SCORE_COLORS["low"]],
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("Student Name:N", title="Student"),
                alt.Tooltip("Score:Q", title="Score"),
            ],
        )
        .properties(height=300)
    )
    st.altair_chart(chart, width="stretch")


def show_risk_chart(dataframe: pd.DataFrame) -> None:
    st.write("Student Risk Levels")
    risk_counts = (
        dataframe["Risk Level"]
        .value_counts()
        .reindex(RISK_ORDER, fill_value=0)
        .rename_axis("Risk Level")
        .reset_index(name="Students")
    )
    chart = (
        alt.Chart(risk_counts)
        .mark_bar(cornerRadiusEnd=4)
        .encode(
            x=alt.X("Students:Q", title="Students", axis=alt.Axis(tickMinStep=1)),
            y=alt.Y("Risk Level:N", title="Risk level", sort=RISK_ORDER),
            color=alt.Color(
                "Risk Level:N",
                scale=alt.Scale(
                    domain=RISK_ORDER,
                    range=[RISK_COLORS[level] for level in RISK_ORDER],
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("Risk Level:N", title="Risk level"),
                alt.Tooltip("Students:Q", title="Students"),
            ],
        )
        .properties(height=300)
    )
    st.altair_chart(chart, width="stretch")