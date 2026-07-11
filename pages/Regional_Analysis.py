import streamlit as st

from analytics.dynamic.regional_analysis import get_revenue_by_region
from analytics.dynamic.customer_analysis import get_top_customer_regions
from insights.regional_insights import generate_regional_insights_text
from visualizations.regional_charts import state_revenue_chart
from visualizations.customer_charts import customer_distribution_chart
from utils.export_utils import get_export_section
from utils.theme import (
    load_css, sidebar_brand, page_header, kpi_row, divider,
    section_header, render_chart, empty_state, summary_card,
)

st.set_page_config(page_title="Regional Analysis", page_icon="🌎", layout="wide")
load_css()
sidebar_brand()
page_header('<i class="ti ti-world"></i>', "Regional Analysis", "Geographic revenue breakdown and AI-powered market intelligence.")

# ── Guard ──
if "df" not in st.session_state or "schema" not in st.session_state:
    empty_state()
    st.stop()

df = st.session_state["df"]
schema = st.session_state["schema"]

region_df = get_revenue_by_region(df, schema)
customer_df = get_top_customer_regions(df, schema)

kpi_row([
    {
        "label": "Top Revenue Region",
        "value": region_df.iloc[0]["region"] if len(region_df) > 0 else "N/A",
        "icon": '<i class="ti ti-currency-dollar"></i>',
    },
    {
        "label": "Top Customer Region",
        "value": customer_df.iloc[0]["region"] if len(customer_df) > 0 else "N/A",
        "icon": '<i class="ti ti-users"></i>',
    },
])

divider()

# ── Revenue by Region ──
section_header("Revenue by Region", '<i class="ti ti-currency-dollar"></i>')
render_chart(state_revenue_chart(region_df))

divider()

# ── Customer Distribution ──
section_header("Customer Distribution", '<i class="ti ti-world"></i>')
render_chart(customer_distribution_chart(customer_df))

# AI Regional Insights
section_header("AI Regional Intelligence", '<i class="ti ti-robot"></i>')
with st.spinner("Analyzing regional performance..."):
    reg_insights = generate_regional_insights_text(df, schema)
summary_card(reg_insights)

# ── Export Section ──
metrics = {
    "top_region_revenue": region_df.iloc[0]["region"] if len(region_df) > 0 else "N/A",
    "top_region_revenue_amount": float(region_df.iloc[0]["revenue"]) if len(region_df) > 0 else 0,
    "top_region_customers": customer_df.iloc[0]["region"] if len(customer_df) > 0 else "N/A",
    "top_region_customer_count": int(customer_df.iloc[0]["customers"]) if len(customer_df) > 0 else 0,
}
summary = (
    f"Top revenue region: {metrics['top_region_revenue']} with ${metrics['top_region_revenue_amount']:,.2f}. "
    f"Top customer region: {metrics['top_region_customers']} with {metrics['top_region_customer_count']:,} customers."
)
get_export_section(df, schema, metrics, summary, page_name="Regional Analysis")
