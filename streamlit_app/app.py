"""Databricks ETL Agent — multipage Streamlit demo entry point (Home)."""

import streamlit as st

from core import STAGE_PAGES, STAGES, page_header, setup_page

setup_page(current_stage=-1)
page_header()

st.header("🏠 Home — Demo Overview")
st.markdown(
    """
This demo walks through the full ETL Agent workflow:

| Step | Page | What happens |
|------|------|--------------|
| 1 | **Ingestion** | Upload a mapping document or describe the pipeline |
| 2 | **Requirements Agent** | Parser agent extracts requirements, asks clarifications |
| 3 | **Validation Gate** | JSON schema checks on the extracted output |
| 4 | **Sample Data Review** | PySpark mock engine preview, approve or reject |
| 5 | **Databricks Pipeline** | Configured pipeline generated from the template |

*Demo mode — no real actions are executed.*
"""
)

st.divider()
if st.button("🚀 Start Demo", type="primary"):
    st.session_state.stage = 0
    st.switch_page(STAGE_PAGES[0])

st.caption(f"Current progress: {STAGES[st.session_state.stage]}")
