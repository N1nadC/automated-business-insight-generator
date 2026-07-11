import pandas as pd


def get_revenue_by_region(df, schema):
    """
    Returns revenue grouped by region.
    """

    region_col = schema.get("region")
    revenue_col = schema.get("revenue")

    if region_col is None:
        raise ValueError("Region column not detected.")

    if revenue_col is None:
        raise ValueError("Revenue column not detected.")

    temp = df.copy()

    temp[revenue_col] = pd.to_numeric(
        temp[revenue_col],
        errors="coerce"
    )

    regional = (
        temp.groupby(region_col)[revenue_col]
        .sum()
        .reset_index()
        .sort_values(revenue_col, ascending=False)
    )

    regional.columns = [
        "region",
        "revenue"
    ]

    return regional


def get_top_region(df, schema):
    """
    Returns the highest revenue generating region.
    """

    regional = get_revenue_by_region(df, schema)

    return {
        "region": regional.iloc[0]["region"],
        "revenue": float(regional.iloc[0]["revenue"])
    }


def get_regional_statistics(df, schema):
    """
    Returns regional KPIs.
    """

    regional = get_revenue_by_region(df, schema)

    return {
        "total_regions": len(regional),
        "top_region": regional.iloc[0]["region"],
        "top_region_revenue": float(regional.iloc[0]["revenue"])
    }
    