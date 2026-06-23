import streamlit as st

from analytics.regional_analysis import revenue_by_state
from analytics.customer_analysis import top_customer_states

from visualizations.regional_charts import state_revenue_chart
from visualizations.customer_charts import customer_distribution_chart

st.title("🌎 Regional Analysis")

# Revenue by State
st.subheader("Revenue by State")

state_df = revenue_by_state()

fig = state_revenue_chart(state_df)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Customer Distribution
st.subheader("Customer Distribution")

customer_df = top_customer_states()

fig = customer_distribution_chart(customer_df)

st.plotly_chart(fig, use_container_width=True)