import streamlit as st

from analytics.monthly_analysis import get_monthly_sales
from analytics.product_analysis import (
    get_top_products,
    category_performance
)

from visualizations.monthly_charts import monthly_revenue_chart
from visualizations.product_charts import top_products_chart
from visualizations.category_charts import category_performance_chart


st.title("📈 Sales Analysis")

# -----------------------------------
# Monthly Revenue Trend
# -----------------------------------

st.subheader("Monthly Revenue Trend")

monthly_df = get_monthly_sales()

fig = monthly_revenue_chart(monthly_df)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------------
# Category Performance
# -----------------------------------

st.subheader("Category Performance")

category_df = category_performance()

fig = category_performance_chart(category_df)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------------
# Top Products
# -----------------------------------

st.subheader("Top Products")

products_df = get_top_products()

fig = top_products_chart(products_df)

st.plotly_chart(fig, use_container_width=True)