"""Stage 1 — Ingestion: document upload / user input."""

import time

import streamlit as st

from core import goto, page_header, setup_page

setup_page(current_stage=0)
page_header()

st.header("1️⃣ Ingestion — Document Upload / User Input")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Mapping Document")
    uploaded = st.file_uploader(
        "Upload an ETL mapping document",
        type=["pdf", "docx", "xlsx", "csv", "txt"],
    )
    if uploaded:
        st.success(f"Received **{uploaded.name}** ({uploaded.size:,} bytes)")

with col2:
    st.subheader("✍️ Or Describe Your Pipeline")
    user_text = st.text_area(
        "Describe the ETL requirements in plain English",
        placeholder="e.g. Load orders from raw.sales.orders_raw, clean up customer ids, "
        "round amounts, and write to curated.sales.orders_curated nightly at 2 AM...",
        height=160,
    )

st.divider()
if st.button("🚀 Submit to Requirements Agent", type="primary"):
    if not uploaded and not user_text.strip():
        st.warning("Upload a document or enter a description first.")
    else:
        with st.spinner("Sending input to the Requirements Agent..."):
            time.sleep(1)
        goto(1)
