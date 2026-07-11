import pandas as pd


def get_category_performance(df, schema):
    """
    Returns revenue grouped by product category.
    """

    category_col = schema.get("category")
    revenue_col = schema.get("revenue")

    if category_col is None:
        raise ValueError("Category column not detected.")

    if revenue_col is None:
        raise ValueError("Revenue column not detected.")

    temp = df.copy()

    temp[revenue_col] = pd.to_numeric(
        temp[revenue_col],
        errors="coerce"
    )

    category = (
        temp.groupby(category_col)[revenue_col]
        .sum()
        .reset_index()
        .sort_values(revenue_col, ascending=False)
    )

    category.columns = [
        "category",
        "revenue"
    ]

    return category


def get_top_products(df, schema, top_n=10):
    """
    Returns the top N products by revenue.
    """

    product_col = schema.get("product")
    revenue_col = schema.get("revenue")

    if product_col is None:
        raise ValueError("Product column not detected.")

    if revenue_col is None:
        raise ValueError("Revenue column not detected.")

    temp = df.copy()

    temp[revenue_col] = pd.to_numeric(
        temp[revenue_col],
        errors="coerce"
    )

    products = (
        temp.groupby(product_col)[revenue_col]
        .sum()
        .reset_index()
        .sort_values(revenue_col, ascending=False)
        .head(top_n)
    )

    products.columns = [
        "product",
        "revenue"
    ]

    return products


def get_top_category(df, schema):
    """
    Returns the highest revenue generating category.
    """

    category_df = get_category_performance(df, schema)

    return {
        "category": category_df.iloc[0]["category"],
        "revenue": float(category_df.iloc[0]["revenue"])
    }