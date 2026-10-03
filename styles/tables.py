import pandas as pd
import streamlit as st

from .theme import ACCENT, RISK_BACKGROUND_COLORS, RISK_COLORS


def show_styled_table(dataframe: pd.DataFrame) -> None:
    styled_dataframe = dataframe.style
    column_config = {}

    for column, color in (("Score", "#218268"), ("Attendance", ACCENT)):
        if column in dataframe.columns:
            column_config[column] = st.column_config.ProgressColumn(
                column,
                format="%d",
                min_value=0,
                max_value=100,
                color=color,
            )

    if "Risk Level" in dataframe.columns:
        def style_risk(value: str) -> str:
            color = RISK_COLORS.get(value, "#66737b")
            background = RISK_BACKGROUND_COLORS.get(value, "#eef1f3")
            return (
                f"background-color: {background}; "
                f"color: {color}; font-weight: 600;"
            )

        styled_dataframe = styled_dataframe.map(style_risk, subset=["Risk Level"])

    st.dataframe(
        styled_dataframe,
        column_config=column_config,
        width="stretch",
        hide_index=True,
    )