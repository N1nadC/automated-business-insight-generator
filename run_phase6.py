"""
Phase 6 — Visualization Layer Test Runner
Tests all 6 visualization functions with real data from PostgreSQL.
"""

from database.db_connection import get_engine
from analytics.monthly_analysis import get_monthly_sales
from analytics.product_analysis import get_top_products
from analytics.customer_analysis import top_customer_states
from analytics.delivery_analysis import average_delivery_days
from analytics.regional_analysis import revenue_by_state
from analytics.category_analysis import category_performance

from visualizations.monthly_charts import monthly_revenue_chart
from visualizations.product_charts import top_products_chart
from visualizations.customer_charts import customer_distribution_chart
from visualizations.delivery_charts import delivery_gauge
from visualizations.regional_charts import state_revenue_chart
from visualizations.category_charts import category_performance_chart

import plotly.io as pio

# Ensure consistent rendering
pio.templates.default = 'plotly'

print("=" * 60)
print("PHASE 6 — VISUALIZATION LAYER TEST")
print("=" * 60)

# 1. Monthly Revenue Trend
print("\n[1/6] Monthly Revenue Trend...")
monthly_df = get_monthly_sales()
monthly_fig = monthly_revenue_chart(monthly_df)
monthly_fig.write_html("reports/monthly_revenue_trend.html")
print("  ✅ Saved: reports/monthly_revenue_trend.html")

# 2. Top Products
print("\n[2/6] Top Products...")
products_df = get_top_products()
products_fig = top_products_chart(products_df, top_n=10)
products_fig.write_html("reports/top_products.html")
print("  ✅ Saved: reports/top_products.html")

# 3. Customer Distribution
print("\n[3/6] Customer Distribution...")
customers_df = top_customer_states()
customers_fig = customer_distribution_chart(customers_df)
customers_fig.write_html("reports/customer_distribution.html")
print("  ✅ Saved: reports/customer_distribution.html")

# 4. Delivery KPI Gauge
print("\n[4/6] Delivery KPI Gauge...")
delivery_days = average_delivery_days()
# delivery_days is now a float (fixed in analytics/delivery_analysis.py)
delivery_fig = delivery_gauge(delivery_days)
delivery_fig.write_html("reports/delivery_kpi.html")
print(f"  ✅ Average delivery: {delivery_days:.1f} days")
print("  ✅ Saved: reports/delivery_kpi.html")

# 5. Revenue by State
print("\n[5/6] Revenue by State...")
states_df = revenue_by_state()
states_fig = state_revenue_chart(states_df)
states_fig.write_html("reports/revenue_by_state.html")
print("  ✅ Saved: reports/revenue_by_state.html")

# 6. Category Performance
print("\n[6/6] Category Performance...")
categories_df = category_performance()
categories_fig = category_performance_chart(categories_df)
categories_fig.write_html("reports/category_performance.html")
print("  ✅ Saved: reports/category_performance.html")

print("\n" + "=" * 60)
print("ALL 6 VISUALIZATIONS GENERATED SUCCESSFULLY")
print("=" * 60)
