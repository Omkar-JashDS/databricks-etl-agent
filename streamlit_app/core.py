"""Shared helpers, mock data, and sidebar for the multipage demo UI."""

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------
MOCK_REQUIREMENTS_JSON = {
    "pipeline_name": "customer_orders_etl",
    "source": {
        "type": "delta",
        "catalog": "raw",
        "schema": "sales",
        "table": "orders_raw",
    },
    "target": {
        "type": "delta",
        "catalog": "curated",
        "schema": "sales",
        "table": "orders_curated",
        "write_mode": "merge",
    },
    "transformations": [
        {"column": "order_date", "rule": "CAST(order_date AS DATE)"},
        {"column": "amount", "rule": "ROUND(amount, 2)"},
        {"column": "customer_id", "rule": "TRIM(UPPER(customer_id))"},
        {"column": "status", "rule": "COALESCE(status, 'UNKNOWN')"},
    ],
    "data_quality": [
        {"column": "order_id", "check": "NOT NULL"},
        {"column": "amount", "check": ">= 0"},
    ],
    "schedule": "0 2 * * *",
}

MOCK_SAMPLE_DATA = pd.DataFrame(
    {
        "order_id": [1001, 1002, 1003, 1004, 1005],
        "customer_id": ["CUST-001", "CUST-002", "CUST-003", "CUST-001", "CUST-004"],
        "order_date": ["2026-10-01", "2026-10-01", "2026-10-02", "2026-10-03", "2026-10-04"],
        "amount": [249.99, 89.50, 1200.00, 34.25, 560.75],
        "status": ["SHIPPED", "PENDING", "SHIPPED", "UNKNOWN", "DELIVERED"],
    }
)

MOCK_PIPELINE_CODE = '''# Auto-generated Databricks pipeline (demo)
from pyspark.sql import functions as F

df = spark.read.table("raw.sales.orders_raw")

df_curated = (
    df.withColumn("order_date", F.col("order_date").cast("date"))
      .withColumn("amount", F.round("amount", 2))
      .withColumn("customer_id", F.trim(F.upper("customer_id")))
      .withColumn("status", F.coalesce("status", F.lit("UNKNOWN")))
      .filter(F.col("order_id").isNotNull() & (F.col("amount") >= 0))
)

(
    df_curated.write.format("delta")
    .mode("overwrite")
    .saveAsTable("curated.sales.orders_curated")
)
'''

STAGES = [
    "1. Ingestion",
    "2. Requirements Agent",
    "3. Validation Gate",
    "4. Sample Data Review",
    "5. Databricks Pipeline",
]

# Page paths are relative to the main script (app.py)
STAGE_PAGES = [
    "pages/1_Ingestion.py",
    "pages/2_Requirements_Agent.py",
    "pages/3_Validation_Gate.py",
    "pages/4_Sample_Data_Review.py",
    "pages/5_Databricks_Pipeline.py",
]


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------
def init_state() -> None:
    if "stage" not in st.session_state:
        st.session_state.stage = 0


def goto(stage: int) -> None:
    """Unlock a stage and switch to its page."""
    st.session_state.stage = stage
    st.switch_page(STAGE_PAGES[stage])


def require_stage(stage: int) -> None:
    """Block access to pages beyond the currently unlocked stage."""
    if st.session_state.stage < stage:
        st.warning(
            f"🔒 This step is locked. Complete **{STAGES[st.session_state.stage]}** first."
        )
        if st.button(f"Go to {STAGES[st.session_state.stage]}"):
            st.switch_page(STAGE_PAGES[st.session_state.stage])
        st.stop()


# ---------------------------------------------------------------------------
# Shared layout
# ---------------------------------------------------------------------------
def setup_page(current_stage: int | None = None) -> None:
    """Call first on every page: page config, state init, and sidebar."""
    st.set_page_config(
        page_title="Databricks ETL Agent",
        page_icon="⚡",
        layout="wide",
    )
    init_state()

    active = st.session_state.stage if current_stage is None else current_stage

    with st.sidebar:
        st.title("⚡ ETL Agent")
        st.caption(
            "AI system that converts ETL mapping documents into executable Databricks pipelines."
        )
        st.divider()
        st.subheader("Workflow Progress")
        for i, name in enumerate(STAGES):
            if i < st.session_state.stage:
                st.success(name, icon="✅")
            elif i == active:
                st.info(name, icon="▶️")
            else:
                st.markdown(
                    f"<span style='color:grey'>⬜ {name}</span>", unsafe_allow_html=True
                )
        st.divider()
        if st.button("🔄 Restart Demo", use_container_width=True):
            st.session_state.stage = 0
            st.switch_page("app.py")
        st.caption("Demo mode — no real actions are executed.")


def page_header() -> None:
    st.title("Databricks ETL Agent")
    st.caption(
        "Tech stack: Streamlit · Python · PySpark · LLM & Prompt Engineering · Terraform"
    )
    st.divider()
