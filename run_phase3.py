from analytics.revenue_analysis import *
from analytics.monthly_analysis import *
from analytics.product_analysis import *
from analytics.customer_analysis import *
from analytics.delivery_analysis import *
from analytics.regional_analysis import *

print(get_total_revenue())
print(get_average_order_value())

print(get_monthly_sales().head())

print(get_top_products())

print(category_performance().head())

print(total_customers())

print(top_customer_states())

print(average_delivery_days())

print(revenue_by_state())