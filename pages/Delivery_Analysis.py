import streamlit as st

from analytics.delivery_analysis import average_delivery_days
from visualizations.delivery_charts import delivery_gauge

st.title("🚚 Delivery Analysis")

avg_days = average_delivery_days()

st.metric(
    "Average Delivery Days",
    f"{avg_days:.2f}"
)

st.divider()

fig = delivery_gauge(avg_days)

st.plotly_chart(fig, use_container_width=True)