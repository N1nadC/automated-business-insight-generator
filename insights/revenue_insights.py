from analytics.revenue_analysis import (
    get_total_revenue,
    get_average_order_value
)


def revenue_summary():

    revenue = get_total_revenue().iloc[0, 0]
    avg_order = get_average_order_value().iloc[0, 0]

    insight = (
        f"Total revenue generated was ${revenue:,.2f}. "
        f"The average order value was ${avg_order:,.2f}, "
        "indicating healthy customer spending behavior."
    )

    return insight