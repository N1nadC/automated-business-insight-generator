import streamlit as st

from analytics.dashboard_metrics import get_dashboard_metrics
from analytics.monthly_analysis import get_monthly_sales

from visualizations.monthly_charts import monthly_revenue_chart

from reports.executive_summary import generate_executive_summary


st.title("📈 Executive Overview")

metrics = get_dashboard_metrics()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Revenue",
        f"${metrics['total_revenue']:,.2f}"
    )

with col2:
    st.metric(
        "Average Order Value",
        f"${metrics['avg_order_value']:,.2f}"
    )

with col3:
    st.metric(
        "Customers",
        f"{metrics['customers']:,}"
    )


col4, col5 = st.columns(2)

with col4:
    st.metric(
        "Average Delivery Days",
        f"{metrics['avg_delivery_days']:.1f}"
    )

with col5:
    st.metric(
        "Top Category",
        metrics["top_category"]
    )

st.divider()

monthly_df = get_monthly_sales()

fig = monthly_revenue_chart(monthly_df)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("🤖 Executive Summary")

st.text(generate_executive_summary())