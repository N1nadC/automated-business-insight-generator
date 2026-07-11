import pandas as pd


def get_total_customers(df, schema):
    """
    Returns the total number of unique customers.
    """

    customer_col = schema.get("customer")

    if customer_col is None:
        raise ValueError("Customer column not detected.")

    return int(df[customer_col].nunique())


def get_top_customer_regions(df, schema, top_n=10):
    """
    Returns customer count by region.
    """

    customer_col = schema.get("customer")
    region_col = schema.get("region")

    if customer_col is None:
        raise ValueError("Customer column not detected.")

    if region_col is None:
        raise ValueError("Region column not detected.")

    customer_regions = (
        df.groupby(region_col)[customer_col]
        .nunique()
        .reset_index(name="customers")
        .sort_values("customers", ascending=False)
        .head(top_n)
    )

    customer_regions.columns = [
        "region",
        "customers"
    ]

    return customer_regions


def get_customer_statistics(df, schema):
    """
    Returns customer KPIs.
    """

    return {
        "total_customers": get_total_customers(df, schema)
    }