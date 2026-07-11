import pandas as pd


def get_total_revenue(df, schema):
    """
    Calculate the total revenue from the uploaded dataset.
    """

    revenue_col = schema.get("revenue")

    if revenue_col is None:
        raise ValueError("Revenue column not detected.")

    revenue = pd.to_numeric(df[revenue_col], errors="coerce")

    return float(revenue.sum())


def get_average_order_value(df, schema):
    """
    Calculate the average order value.
    """

    revenue_col = schema.get("revenue")

    if revenue_col is None:
        raise ValueError("Revenue column not detected.")

    revenue = pd.to_numeric(df[revenue_col], errors="coerce")

    return float(revenue.mean())


def get_revenue_statistics(df, schema):
    """
    Return all revenue-related KPIs.
    """

    revenue_col = schema.get("revenue")

    if revenue_col is None:
        raise ValueError("Revenue column not detected.")

    revenue = pd.to_numeric(df[revenue_col], errors="coerce")

    return {
        "total_revenue": float(revenue.sum()),
        "average_order_value": float(revenue.mean()),
        "minimum_order_value": float(revenue.min()),
        "maximum_order_value": float(revenue.max()),
        "median_order_value": float(revenue.median()),
        "total_transactions": int(revenue.count())
    }