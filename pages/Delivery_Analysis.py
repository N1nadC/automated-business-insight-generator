import streamlit as st

from analytics.dynamic.delivery_analysis import get_average_delivery_days
from insights.delivery_insights import generate_delivery_insights_text
from visualizations.delivery_charts import delivery_gauge
from utils.export_utils import get_export_section
from utils.theme import (
    load_css, sidebar_brand, page_header, kpi_row, divider,
    section_header, render_chart, empty_state, summary_card,
)

st.set_page_config(page_title="Delivery Analysis", page_icon="🚚", layout="wide")
load_css()
sidebar_brand()
page_header('<i class="ti ti-truck"></i>', "Delivery Analysis", "Shipping performance and AI-powered logistics intelligence.")

# ── Guard ──
if "df" not in st.session_state or "schema" not in st.session_state:
    empty_state()
    st.stop()

df = st.session_state["df"]
schema = st.session_state["schema"]

# ── KPI ──
avg_days = get_average_delivery_days(df, schema)
kpi_row([
    {"label": "Average Delivery Days", "value": f"{avg_days:.2f}", "icon": '<i class="ti ti-truck"></i>'},
])

divider()

# ── Delivery Gauge ──
section_header("Delivery Performance", '<i class="ti ti-chart-bar"></i>')
fig = delivery_gauge(avg_days)
render_chart(fig)

# AI Delivery Insights
section_header("AI Delivery Intelligence", '<i class="ti ti-robot"></i>')
with st.spinner("Analyzing delivery performance..."):
    del_insights = generate_delivery_insights_text(df, schema)
summary_card(del_insights)

# ── Export Section ──
metrics = {
    "average_delivery_days": avg_days,
}
summary = f"Average delivery time is {avg_days:.1f} days."
get_export_section(df, schema, metrics, summary, page_name="Delivery Analysis")
