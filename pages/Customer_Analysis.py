import streamlit as st

from analytics.dynamic.customer_analysis import get_total_customers, get_top_customer_regions
from insights.customer_insights import generate_customer_insights_text
from visualizations.customer_charts import customer_distribution_chart
from utils.export_utils import get_export_section
from utils.theme import (
    load_css, sidebar_brand, page_header, kpi_row, divider,
    section_header, render_chart, empty_state, summary_card,
)

st.set_page_config(page_title="Customer Analysis", page_icon="👥", layout="wide")
load_css()
sidebar_brand()
page_header('<i class="ti ti-users"></i>', "Customer Analysis", "Customer behavior, segmentation, and AI-powered retention intelligence.")

# ── Guard ──
if "df" not in st.session_state or "schema" not in st.session_state:
    empty_state()
    st.stop()

df = st.session_state["df"]
schema = st.session_state["schema"]

# ── KPI ──
customers = get_total_customers(df, schema)
customer_df = get_top_customer_regions(df, schema)

kpi_row([
    {"label": "Total Customers", "value": f"{customers:,}", "icon": '<i class="ti ti-users"></i>'},
    {
        "label": "Top Region",
        "value": customer_df.iloc[0]["region"] if len(customer_df) > 0 else "N/A",
        "icon": '<i class="ti ti-map-pin"></i>',
    },
])

divider()

# ── Customer Distribution ──
section_header("Customer Distribution", '<i class="ti ti-world"></i>')
render_chart(customer_distribution_chart(customer_df))

# AI Customer Insights
section_header("AI Customer Intelligence", '<i class="ti ti-robot"></i>')
with st.spinner("Analyzing customer behavior..."):
    cust_insights = generate_customer_insights_text(df, schema)
summary_card(cust_insights)

# ── Export Section ──
metrics = {
    "total_customers": customers,
    "top_region": customer_df.iloc[0]["region"] if len(customer_df) > 0 else "N/A",
    "top_region_customers": int(customer_df.iloc[0]["customers"]) if len(customer_df) > 0 else 0,
}
summary = f"Total customers: {customers:,}. Top region: {metrics['top_region']} with {metrics['top_region_customers']:,} customers."
get_export_section(df, schema, metrics, summary, page_name="Customer Analysis")
