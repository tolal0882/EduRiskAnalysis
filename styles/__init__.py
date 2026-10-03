from pathlib import Path

import streamlit as st


def load_css() -> None:
    stylesheet_path = Path(__file__).with_name("style.css")
    stylesheet = stylesheet_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{stylesheet}</style>", unsafe_allow_html=True)