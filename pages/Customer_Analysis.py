import streamlit as st

from analytics.customer_analysis import (
    total_customers,
    top_customer_states
)

from visualizations.customer_charts import customer_distribution_chart

st.title("👥 Customer Analysis")

customers = total_customers()

st.metric(
    "Total Customers",
    f"{customers:,}"
)

st.divider()

customer_df = top_customer_states()

fig = customer_distribution_chart(customer_df)

st.plotly_chart(fig, use_container_width=True)
