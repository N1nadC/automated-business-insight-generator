from analytics.product_analysis import (
    category_performance
)


def product_summary():

    df = category_performance()

    category = df.iloc[0]["product_category_name_english"]
    revenue = df.iloc[0]["revenue"]

    insight = (
        f"The highest-performing category was '{category}', "
        f"which generated ${revenue:,.2f} in revenue."
    )

    return insight