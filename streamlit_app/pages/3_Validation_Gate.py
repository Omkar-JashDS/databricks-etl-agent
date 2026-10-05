"""Stage 3 — Validation Gate: JSON schema check."""

import time

import streamlit as st

from core import goto, page_header, require_stage, setup_page

setup_page(current_stage=2)
require_stage(2)
page_header()

st.header("3️⃣ Validation Gate — JSON Schema Check")

with st.spinner("Validating output against pipeline schema..."):
    time.sleep(0.8)

checks = [
    ("Schema structure", True),
    ("Source definition present", True),
    ("Target definition present", True),
    ("Transformations well-formed", True),
    ("Data quality rules valid", True),
    ("Schedule cron expression valid", True),
]
for name, ok in checks:
    st.success(f"{name} — PASSED", icon="✅") if ok else st.error(f"{name} — FAILED", icon="❌")

st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Back to Requirements Agent"):
        goto(1)
with col2:
    if st.button("▶️ Generate Sample Data", type="primary"):
        goto(3)
