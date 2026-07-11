import streamlit as st

from analytics.dynamic.monthly_analysis import get_monthly_sales
from analytics.dynamic.product_analysis import get_top_products, get_category_performance
from insights.revenue_insights import generate_revenue_insights_text
from insights.product_insights import generate_product_insights_text
from visualizations.monthly_charts import monthly_revenue_chart
from visualizations.product_charts import top_products_chart
from visualizations.category_charts import category_performance_chart
from utils.export_utils import get_export_section
from utils.theme import (
    load_css, sidebar_brand, page_header, divider,
    section_header, render_chart, empty_state, summary_card,
)

st.set_page_config(page_title="Sales Analysis", page_icon="📈", layout="wide")
load_css()
sidebar_brand()
page_header('<i class="ti ti-chart-line"></i>', "Sales Analysis", "Revenue trends and product performance with AI-generated intelligence.")

# ── Guard ──
if "df" not in st.session_state or "schema" not in st.session_state:
    empty_state()
    st.stop()

df = st.session_state["df"]
schema = st.session_state["schema"]

# ── Monthly Revenue Trend ──
section_header("Monthly Revenue Trend", '<i class="ti ti-chart-bar"></i>')
monthly_df = get_monthly_sales(df, schema)
render_chart(monthly_revenue_chart(monthly_df))

# AI Revenue Insights
section_header("AI Revenue Intelligence", '<i class="ti ti-robot"></i>')
with st.spinner("Analyzing revenue trends..."):
    rev_insights = generate_revenue_insights_text(df, schema)
summary_card(rev_insights)

divider()

# ── Category Performance ──
section_header("Category Performance", '<i class="ti ti-folder"></i>')
category_df = get_category_performance(df, schema)
render_chart(category_performance_chart(category_df))

divider()

# ── Top Products ──
section_header("Top Products", '<i class="ti ti-trophy"></i>')
products_df = get_top_products(df, schema)
render_chart(top_products_chart(products_df))

# AI Product Insights
section_header("AI Product Intelligence", '<i class="ti ti-robot"></i>')
with st.spinner("Analyzing product portfolio..."):
    prod_insights = generate_product_insights_text(df, schema)
summary_card(prod_insights)

# ── Export Section ──
metrics = {
    "total_revenue": float(df[schema.get("revenue", df.columns[0])].sum()),
    "top_category": category_df.iloc[0]["category"] if len(category_df) > 0 else "N/A",
    "top_product": products_df.iloc[0]["product"] if len(products_df) > 0 else "N/A",
}
get_export_section(df, schema, metrics, "Sales Analysis Report", page_name="Sales Analysis")
