import streamlit as st

from analytics.dashboard_metrics import get_dashboard_metrics
from analytics.product_analysis import (
    get_top_products,
    category_performance
)

from visualizations.product_charts import top_products_chart
from visualizations.category_charts import category_performance_chart

st.title("🛒 Product Analysis")

# KPI
metrics = get_dashboard_metrics()

st.metric(
    "Top Performing Category",
    metrics["top_category"]
)

st.divider()

# Category Performance
st.subheader("Category Performance")

category_df = category_performance()

fig = category_performance_chart(category_df)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Top Products
st.subheader("Top Products")

products_df = get_top_products()

fig = top_products_chart(products_df)

st.plotly_chart(fig, use_container_width=True)