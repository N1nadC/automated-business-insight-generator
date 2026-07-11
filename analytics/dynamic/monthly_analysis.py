import pandas as pd


def get_monthly_sales(df, schema):
    """
    Generate monthly revenue from uploaded dataset.
    """

    date_col = schema.get("date")
    revenue_col = schema.get("revenue")

    if date_col is None:
        raise ValueError("Date column not detected.")

    if revenue_col is None:
        raise ValueError("Revenue column not detected.")

    temp = df.copy()

    temp[date_col] = pd.to_datetime(
        temp[date_col],
        errors="coerce"
    )

    temp[revenue_col] = pd.to_numeric(
        temp[revenue_col],
        errors="coerce"
    )

    monthly_sales = (
        temp
        .groupby(temp[date_col].dt.to_period("M"))[revenue_col]
        .sum()
        .reset_index()
    )

    monthly_sales[date_col] = (
        monthly_sales[date_col]
        .dt.to_timestamp()
    )

    monthly_sales.columns = [
        "month",
        "revenue"
    ]

    return monthly_sales