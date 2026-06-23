from analytics.revenue_analysis import (
    get_total_revenue,
    get_average_order_value
)

from analytics.customer_analysis import (
    total_customers
)

from analytics.delivery_analysis import (
    average_delivery_days
)

from analytics.product_analysis import (
    category_performance
)


def get_dashboard_metrics():
    """
    Returns a dictionary of key dashboard metrics.

    Returns
    -------
    dict
        Dictionary containing:
        - total_revenue (float)
        - avg_order_value (float)
        - customers (int)
        - avg_delivery_days (float)
        - top_category (str)
        - top_category_revenue (float)
    """
    total_revenue = get_total_revenue().iloc[0, 0]

    avg_order_value = get_average_order_value().iloc[0, 0]

    # total_customers() now returns int directly (not a DataFrame)
    customers = total_customers()

    # average_delivery_days() now returns float directly (not a DataFrame)
    avg_delivery = average_delivery_days()

    top_category = category_performance().iloc[0][
        "product_category_name_english"
    ]

    top_category_revenue = category_performance().iloc[0][
        "revenue"
    ]

    return {
        "total_revenue": total_revenue,
        "avg_order_value": avg_order_value,
        "customers": customers,
        "avg_delivery_days": avg_delivery,
        "top_category": top_category,
        "top_category_revenue": top_category_revenue
    }