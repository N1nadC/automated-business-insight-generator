from analytics.customer_analysis import total_customers


def customer_summary():
    """
    Generates a natural-language summary of customer metrics.

    Returns
    -------
    str
        Formatted customer insight summary.
    """
    customers = total_customers()

    return (
        f"The business serves a total of {customers:,} customers, "
        f"reflecting the scale of the customer base."
    )