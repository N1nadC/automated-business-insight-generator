import streamlit as st
import pandas as pd
from analytics.schema_detector import detect_schema
from utils.theme import (
    load_css, sidebar_brand, page_header, kpi_row,
    divider, section_header, nav_card,
)

st.set_page_config(
    page_title="Business Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()
sidebar_brand()

page_header(
    '<i class="ti ti-chart-infographic"></i>',
    "Business Analytics Dashboard",
    "Upload a dataset to unlock KPIs, visual analytics, and AI-generated insights.",
)

# ── Dataset Upload ──
uploaded_file = st.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xlsx", "xls"],
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        schema = detect_schema(df)
        st.session_state["df"] = df
        st.session_state["schema"] = schema

        st.success(
            f"Dataset loaded — **{len(df):,}** rows and **{len(df.columns)}** columns detected. "
            f"Use the sidebar to explore."
        )

        kpi_row([
            {"label": "Rows", "value": f"{len(df):,}", "icon": '<i class="ti ti-receipt"></i>'},
            {"label": "Columns", "value": f"{len(df.columns):,}", "icon": '<i class="ti ti-folder"></i>'},
            {"label": "Detected Fields", "value": f"{len(schema):,}", "icon": '<i class="ti ti-dna"></i>'},
        ])

        divider()

        col1, col2 = st.columns(2)
        with col1:
            with st.expander("Preview Dataset", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)
        with col2:
            with st.expander("Detected Schema", expanded=True):
                st.json(schema)

    except Exception as e:
        st.error(f"Failed to load file: {e}")

else:
    st.session_state.pop("df", None)
    st.session_state.pop("schema", None)
    st.info("No dataset uploaded yet. Drop a CSV or Excel file above to get started.")

divider()

section_header("Available Pages", '<i class="ti ti-files"></i>')

pages = [
    ('<i class="ti ti-chart-line"></i>', "Executive Overview", "High-level KPIs and performance summary"),
    ('<i class="ti ti-chart-bar"></i>', "Sales Analysis", "Revenue trends and product performance"),
    ('<i class="ti ti-shopping-cart"></i>', "Product Analysis", "Category and top product insights"),
    ('<i class="ti ti-users"></i>', "Customer Analysis", "Customer distribution and metrics"),
    ('<i class="ti ti-world"></i>', "Regional Analysis", "Geographic revenue and customer data"),
    ('<i class="ti ti-truck"></i>', "Delivery Analysis", "Shipping and delivery metrics"),
    ('<i class="ti ti-robot"></i>', "AI Insights", "AI-generated executive summaries"),
]

cols = st.columns(3)
for i, (icon, title, desc) in enumerate(pages):
    with cols[i % 3]:
        nav_card(icon, title, desc)
