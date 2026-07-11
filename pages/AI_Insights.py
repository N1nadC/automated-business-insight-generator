import streamlit as st

from insights.executive_insights import generate_comprehensive_insights
from reports.executive_summary import generate_executive_summary
from utils.export_utils import get_export_section
from utils.theme import (
    load_css, sidebar_brand, page_header, divider,
    section_header, empty_state, summary_card, signal_card,
)

st.set_page_config(page_title="AI Business Insights", page_icon="🤖", layout="wide")
load_css()
sidebar_brand()
page_header('<i class="ti ti-robot"></i>', "AI Business Insights", "Comprehensive AI-generated strategic intelligence across all business dimensions.")

# ── Guard ──
if "df" not in st.session_state or "schema" not in st.session_state:
    empty_state()
    st.stop()

df = st.session_state["df"]
schema = st.session_state["schema"]

# ── Comprehensive AI Intelligence ──
section_header("Executive Strategic Briefing", '<i class="ti ti-target"></i>')
with st.spinner("Generating comprehensive business intelligence..."):
    insights = generate_comprehensive_insights(df, schema)

summary_card(insights['executive_summary'])

divider()

# Strategic Dashboard
section_header("Strategic Control Panel", "")
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

# Dimension Tabs
section_header("Deep-Dive Intelligence", '<i class="ti ti-search"></i>')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Revenue", "Product", "Customer", "Regional", "Delivery"])

with tab1:
    if "error" not in insights["revenue"]:
        summary_card("\n".join(insights["revenue"]["findings"]))
        if insights["revenue"]["recommendations"]:
            st.markdown("**Recommendations**")
            for rec in insights["revenue"]["recommendations"][:3]:
                signal_card(rec, "priority")
        if insights["revenue"]["risks"]:
            st.markdown("**Risks**")
            for risk in insights["revenue"]["risks"][:3]:
                signal_card(risk, "risk")
    else:
        st.warning(insights["revenue"]["error"])

with tab2:
    if "error" not in insights["product"]:
        summary_card("\n".join(insights["product"]["findings"]))
        if insights["product"]["recommendations"]:
            st.markdown("**Recommendations**")
            for rec in insights["product"]["recommendations"][:3]:
                signal_card(rec, "priority")
        if insights["product"]["risks"]:
            st.markdown("**Risks**")
            for risk in insights["product"]["risks"][:3]:
                signal_card(risk, "risk")
    else:
        st.warning(insights["product"]["error"])

with tab3:
    if "error" not in insights["customer"]:
        summary_card("\n".join(insights["customer"]["findings"]))
        if insights["customer"]["recommendations"]:
            st.markdown("**Recommendations**")
            for rec in insights["customer"]["recommendations"][:3]:
                signal_card(rec, "priority")
        if insights["customer"]["risks"]:
            st.markdown("**Risks**")
            for risk in insights["customer"]["risks"][:3]:
                signal_card(risk, "risk")
    else:
        st.warning(insights["customer"]["error"])

with tab4:
    if "error" not in insights["regional"]:
        summary_card("\n".join(insights["regional"]["findings"]))
        if insights["regional"]["recommendations"]:
            st.markdown("**Recommendations**")
            for rec in insights["regional"]["recommendations"][:3]:
                signal_card(rec, "priority")
        if insights["regional"]["risks"]:
            st.markdown("**Risks**")
            for risk in insights["regional"]["risks"][:3]:
                signal_card(risk, "risk")
    else:
        st.warning(insights["regional"]["error"])

with tab5:
    if "error" not in insights["delivery"]:
        summary_card("\n".join(insights["delivery"]["findings"]))
        if insights["delivery"]["recommendations"]:
            st.markdown("**Recommendations**")
            for rec in insights["delivery"]["recommendations"][:3]:
                signal_card(rec, "priority")
        if insights["delivery"]["risks"]:
            st.markdown("**Risks**")
            for risk in insights["delivery"]["risks"][:3]:
                signal_card(risk, "risk")
    else:
        st.warning(insights["delivery"]["error"])

# ── Export Section ──
metrics = {
    "total_revenue": float(df[schema.get("revenue", df.columns[0])].sum()),
    "total_customers": df[schema.get("customer", df.columns[0])].nunique() if schema.get("customer") else len(df),
}
summary = generate_executive_summary(df, schema)
get_export_section(df, schema, metrics, summary, page_name="AI Insights")
