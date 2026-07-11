from analytics.dynamic.revenue_analysis import (
    get_total_revenue,
    get_average_order_value
)

from analytics.dynamic.customer_analysis import (
    get_total_customers
)

from analytics.dynamic.delivery_analysis import (
    get_average_delivery_days
)


def get_dashboard_metrics(df, schema):
    """
    Generate all dashboard KPIs from the uploaded dataset.
    Returns the EXACT same key names as the SQL version
    so that all pages work without modification.
    """

    # Lazy import to avoid circular dependency with product_analysis
    from analytics.dynamic.product_analysis import get_top_category

    top_category = get_top_category(df, schema)

    metrics = {
        "total_revenue": get_total_revenue(df, schema),
        "avg_order_value": get_average_order_value(df, schema),
        "customers": get_total_customers(df, schema),
        "avg_delivery_days": get_average_delivery_days(df, schema),
        "top_category": top_category["category"],
        "top_category_revenue": top_category["revenue"]
    }

    return metrics