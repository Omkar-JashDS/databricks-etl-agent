"""Stage 4 — Sample Data Review: PySpark mock engine preview."""

import streamlit as st

from core import MOCK_SAMPLE_DATA, goto, page_header, require_stage, setup_page

setup_page(current_stage=3)
require_stage(3)
page_header()

st.header("4️⃣ Sample Data Review — PySpark Mock Engine")
st.caption("Preview of transformed output produced by the mock engine (demo data).")

st.dataframe(MOCK_SAMPLE_DATA, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Rows Sampled", "5")
col2.metric("Transformations Applied", "4")
col3.metric("DQ Checks Passed", "2 / 2")

st.divider()
st.subheader("Does this output look correct?")
col1, col2 = st.columns(2)
with col1:
    if st.button("❌ Reject — Back to Parser Agent"):
        goto(1)
with col2:
    if st.button("✅ Approve — Build Pipeline", type="primary"):
        goto(4)
