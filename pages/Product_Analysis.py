import streamlit as st

from analytics.dynamic.dashboard_metrics import get_dashboard_metrics
from analytics.dynamic.product_analysis import get_top_products, get_category_performance
from insights.product_insights import generate_product_insights_text
from visualizations.product_charts import top_products_chart
from visualizations.category_charts import category_performance_chart
from utils.export_utils import get_export_section
from utils.theme import (
    load_css, sidebar_brand, page_header, kpi_row, divider,
    section_header, render_chart, empty_state, summary_card,
)

st.set_page_config(page_title="Product Analysis", page_icon="🛒", layout="wide")
load_css()
sidebar_brand()
page_header('<i class="ti ti-shopping-cart"></i>', "Product Analysis", "Category and top-product performance with AI-powered portfolio insights.")

# ── Guard ──
if "df" not in st.session_state or "schema" not in st.session_state:
    empty_state()
    st.stop()

df = st.session_state["df"]
schema = st.session_state["schema"]

# ── KPI ──
metrics = get_dashboard_metrics(df, schema)
kpi_row([
    {"label": "Top Performing Category", "value": metrics["top_category"], "icon": '<i class="ti ti-trophy"></i>'},
])

divider()

# ── Category Performance ──
section_header("Category Performance", '<i class="ti ti-folder"></i>')
category_df = get_category_performance(df, schema)
render_chart(category_performance_chart(category_df))

divider()

# ── Top Products ──
section_header("Top Products", '<i class="ti ti-package"></i>')
products_df = get_top_products(df, schema)
render_chart(top_products_chart(products_df))

# AI Product Insights
section_header("AI Product Intelligence", '<i class="ti ti-robot"></i>')
with st.spinner("Analyzing product portfolio..."):
    prod_insights = generate_product_insights_text(df, schema)
summary_card(prod_insights)

# ── Export Section ──
summary = f"Top Category: {metrics['top_category']} with ${metrics['top_category_revenue']:,.2f} revenue."
get_export_section(df, schema, metrics, summary, page_name="Product Analysis")
