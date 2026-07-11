import streamlit as st

from analytics.dynamic.dashboard_metrics import get_dashboard_metrics
from analytics.dynamic.monthly_analysis import get_monthly_sales
from reports.executive_summary import generate_executive_summary
from insights.executive_insights import generate_comprehensive_insights
from visualizations.monthly_charts import monthly_revenue_chart
from utils.export_utils import get_export_section
from utils.theme import (
    load_css, sidebar_brand, page_header, kpi_row, divider,
    section_header, render_chart, empty_state, summary_card, signal_card,
)

st.set_page_config(page_title="Executive Overview", page_icon="📈", layout="wide")
load_css()
sidebar_brand()
page_header('<i class="ti ti-chart-line"></i>', "Executive Overview", "A high-level snapshot of overall business performance with AI-powered strategic insights.")

# ── Guard ──
if "df" not in st.session_state or "schema" not in st.session_state:
    empty_state()
    st.stop()

df = st.session_state["df"]
schema = st.session_state["schema"]

# ── KPI Cards ──
metrics = get_dashboard_metrics(df, schema)

kpi_row([
    {"label": "Total Revenue", "value": f"${metrics['total_revenue']:,.2f}", "icon": '<i class="ti ti-currency-dollar"></i>'},
    {"label": "Avg Order Value", "value": f"${metrics['avg_order_value']:,.2f}", "icon": '<i class="ti ti-calculator"></i>'},
    {"label": "Customers", "value": f"{metrics['customers']:,}", "icon": '<i class="ti ti-users"></i>'},
])
kpi_row([
    {"label": "Avg Delivery Days", "value": f"{metrics['avg_delivery_days']:.1f}", "icon": '<i class="ti ti-truck"></i>'},
    {"label": "Top Category", "value": metrics["top_category"], "icon": '<i class="ti ti-trophy"></i>'},
])

divider()

# ── Monthly Revenue Chart ──
section_header("Monthly Revenue Trend", '<i class="ti ti-chart-bar"></i>')
monthly_df = get_monthly_sales(df, schema)
fig = monthly_revenue_chart(monthly_df)
render_chart(fig)

divider()

# ── AI Strategic Insights ──
section_header("AI Strategic Insights", '<i class="ti ti-robot"></i>')
with st.spinner("Generating comprehensive business intelligence..."):
    insights = generate_comprehensive_insights(df, schema)

# Executive Briefing
summary_card(insights['executive_summary'])

divider()

# Risk Dashboard
section_header("Strategic Dashboard", "")
cols = st.columns(3)
with cols[0]:
    st.markdown("**Critical Risks**")
    for risk in insights["critical_risks"][:3]:
        signal_card(risk, "risk")
    if not insights["critical_risks"]:
        signal_card("No critical risks detected.", "note")

with cols[1]:
    st.markdown("**Strategic Priorities**")
    for rec in insights["strategic_recommendations"][:3]:
        signal_card(rec, "priority")
    if not insights["strategic_recommendations"]:
        signal_card("No urgent priorities.", "note")

with cols[2]:
    st.markdown("**Quick Wins**")
    for opp in insights["top_opportunities"][:3]:
        signal_card(opp, "opportunity")
    if not insights["top_opportunities"]:
        signal_card("No immediate opportunities flagged.", "note")

divider()

# ── Detailed Dimension Reports ──
section_header("Deep-Dive Intelligence", '<i class="ti ti-search"></i>')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Revenue", "Product", "Customer", "Regional", "Delivery"])

with tab1:
    if "error" not in insights["revenue"]:
        summary_card("\n".join(insights["revenue"]["findings"]))
    else:
        st.warning(insights["revenue"]["error"])

with tab2:
    if "error" not in insights["product"]:
        summary_card("\n".join(insights["product"]["findings"]))
    else:
        st.warning(insights["product"]["error"])

with tab3:
    if "error" not in insights["customer"]:
        summary_card("\n".join(insights["customer"]["findings"]))
    else:
        st.warning(insights["customer"]["error"])

with tab4:
    if "error" not in insights["regional"]:
        summary_card("\n".join(insights["regional"]["findings"]))
    else:
        st.warning(insights["regional"]["error"])

with tab5:
    if "error" not in insights["delivery"]:
        summary_card("\n".join(insights["delivery"]["findings"]))
    else:
        st.warning(insights["delivery"]["error"])

divider()

# ── Executive Summary (Legacy) ──
section_header("Executive Summary", '<i class="ti ti-notes"></i>')
summary = generate_executive_summary(df, schema)
summary_card(summary)

# ── Export Section ──
get_export_section(df, schema, metrics, summary, page_name="Executive Overview")
