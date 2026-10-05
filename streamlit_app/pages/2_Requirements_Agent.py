"""Stage 2 — Requirements Agent: parsing & clarification."""

import time

import streamlit as st

from core import MOCK_REQUIREMENTS_JSON, goto, page_header, require_stage, setup_page

setup_page(current_stage=1)
require_stage(1)
page_header()

st.header("2️⃣ Requirements Agent — Parsing & Clarification")

with st.status("Parser Agent running...", expanded=True) as status:
    st.write("🔍 Extracting source and target definitions...")
    time.sleep(0.4)
    st.write("🧠 Identifying transformation rules...")
    time.sleep(0.4)
    st.write("❓ Checking for missing information...")
    time.sleep(0.4)
    status.update(label="Parsing complete", state="complete")

st.subheader("Clarification Questions")
st.info("The agent found one ambiguity and needs your input (demo).")
st.radio(
    "What write mode should be used for the target table?",
    ["merge (upsert)", "overwrite", "append"],
    horizontal=True,
)
st.text_input("Any additional notes for the agent? (optional)")

st.subheader("Extracted Requirements (JSON)")
st.json(MOCK_REQUIREMENTS_JSON)

st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Back to Ingestion"):
        goto(0)
with col2:
    if st.button("✅ Confirm & Validate JSON", type="primary"):
        goto(2)
