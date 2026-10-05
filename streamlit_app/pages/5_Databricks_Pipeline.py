"""Stage 5 — Databricks Pipeline: generated & configured."""

import json
import time

import streamlit as st

from core import (
    MOCK_PIPELINE_CODE,
    MOCK_REQUIREMENTS_JSON,
    page_header,
    require_stage,
    setup_page,
)

setup_page(current_stage=4)
require_stage(4)
page_header()

st.header("5️⃣ Databricks Pipeline — Generated & Configured")

with st.status("Configuring pipeline...", expanded=True) as status:
    st.write("📋 Loading base pipeline template...")
    time.sleep(0.4)
    st.write("⚙️ Injecting configuration from approved JSON...")
    time.sleep(0.4)
    st.write("🏗️ Rendering Terraform deployment plan...")
    time.sleep(0.4)
    status.update(label="Pipeline configured", state="complete")

st.balloons()
st.success("Databricks pipeline generated successfully! (demo)")

tab1, tab2 = st.tabs(["🐍 Generated PySpark Code", "📦 Pipeline Config"])
with tab1:
    st.code(MOCK_PIPELINE_CODE, language="python")
with tab2:
    st.json(MOCK_REQUIREMENTS_JSON)

st.download_button(
    "⬇️ Download Pipeline Config (JSON)",
    data=json.dumps(MOCK_REQUIREMENTS_JSON, indent=2),
    file_name="pipeline_config.json",
    mime="application/json",
)

st.divider()
if st.button("🔄 Start New Pipeline", type="primary"):
    st.session_state.stage = 0
    st.switch_page("app.py")
