# from insights.revenue_insights import revenue_summary
# from insights.product_insights import product_summary
# from insights.regional_insights import regional_summary
# from insights.customer_insights import customer_summary
# from insights.delivery_insights import delivery_summary


# def generate_executive_summary(df=None, schema=None):
#     """
#     Generate executive summary.

#     If df and schema are provided (dynamic mode), uses the uploaded dataset.
#     Otherwise falls back to SQL mode (legacy).
#     """

#     if df is not None and schema is not None:
#         # Dynamic mode — build summary from DataFrame
#         import pandas as pd

#         # Revenue
#         revenue_col = schema.get("revenue_column")
#         total_revenue = df[revenue_col].sum() if revenue_col else 0

#         # Customers
#         customer_col = schema.get("customer_column")
#         total_customers = df[customer_col].nunique() if customer_col else 0

#         # AOV
#         order_col = schema.get("order_id_column")
#         if order_col and revenue_col:
#             total_orders = df[order_col].nunique()
#             aov = total_revenue / total_orders if total_orders > 0 else 0
#         else:
#             aov = 0

#         # Top category
#         category_col = schema.get("category_column")
#         if category_col and revenue_col:
#             top_category = df.groupby(category_col)[revenue_col].sum().idxmax()
#             top_category_revenue = df.groupby(category_col)[revenue_col].sum().max()
#         else:
#             top_category = "N/A"
#             top_category_revenue = 0

#         # Delivery
#         delivery_col = schema.get("delivery_days_column")
#         if delivery_col:
#             avg_delivery = df[delivery_col].mean()
#         else:
#             avg_delivery = 0

#         # Regional
#         region_col = schema.get("region_column") or schema.get("state_column")
#         if region_col and revenue_col:
#             top_region = df.groupby(region_col)[revenue_col].sum().idxmax()
#             top_region_revenue = df.groupby(region_col)[revenue_col].sum().max()
#         else:
#             top_region = "N/A"
#             top_region_revenue = 0

#         summary = f"""
# ==================================================
# EXECUTIVE BUSINESS SUMMARY
# ==================================================

# REVENUE PERFORMANCE
# -------------------
# Total Revenue: ${total_revenue:,.2f}
# Average Order Value: ${aov:,.2f}
# Total Customers: {total_customers:,}

# PRODUCT PERFORMANCE
# -------------------
# Top Category: {top_category}
# Top Category Revenue: ${top_category_revenue:,.2f}

# REGIONAL PERFORMANCE
# -------------------
# Top Region: {top_region}
# Top Region Revenue: ${top_region_revenue:,.2f}

# CUSTOMER ANALYSIS
# -------------------
# Total Unique Customers: {total_customers:,}

# DELIVERY PERFORMANCE
# -------------------
# Average Delivery Days: {avg_delivery:.1f}

# ==================================================
# END OF REPORT
# ==================================================
# """
#         return summary

#     # SQL mode (legacy) — no arguments
#     summary = f"""
# ==================================================
# EXECUTIVE BUSINESS SUMMARY
# ==================================================

# REVENUE PERFORMANCE
# -------------------
# {revenue_summary()}

# PRODUCT PERFORMANCE
# -------------------
# {product_summary()}

# REGIONAL PERFORMANCE
# -------------------
# {regional_summary()}

# CUSTOMER ANALYSIS
# -------------------
# {customer_summary()}

# DELIVERY PERFORMANCE
# -------------------
# {delivery_summary()}

# ==================================================
# END OF REPORT
# ==================================================
# """
#     return summary


from insights.revenue_insights import revenue_summary
from insights.product_insights import product_summary
from insights.regional_insights import regional_summary
from insights.customer_insights import customer_summary
from insights.delivery_insights import delivery_summary


def generate_executive_summary(df=None, schema=None):
    """
    Generate executive summary.

    If df and schema are provided (dynamic mode), uses the uploaded dataset.
    Otherwise falls back to SQL mode (legacy).
    """

    if df is not None and schema is not None:
        # Dynamic mode — build summary from DataFrame using schema keys:
        # "revenue", "date", "customer", "product", "category", "region", "delivery"

        import pandas as pd

        revenue_col = schema.get("revenue")
        customer_col = schema.get("customer")
        category_col = schema.get("category")
        region_col = schema.get("region")
        delivery_col = schema.get("delivery")
        date_col = schema.get("date")

        # Revenue
        total_revenue = df[revenue_col].sum() if revenue_col else 0

        # Customers
        total_customers = df[customer_col].nunique() if customer_col else 0

        # AOV — use number of rows as proxy for orders if no order_id
        total_orders = len(df)
        aov = total_revenue / total_orders if total_orders > 0 else 0

        # Top category
        if category_col and revenue_col:
            top_category = df.groupby(category_col)[revenue_col].sum().idxmax()
            top_category_revenue = df.groupby(category_col)[revenue_col].sum().max()
        else:
            top_category = "N/A"
            top_category_revenue = 0

        # Delivery — compute days between order date and delivery date
        avg_delivery = 0
        if delivery_col and date_col:
            try:
                order_dates = pd.to_datetime(df[date_col], errors="coerce")
                delivery_dates = pd.to_datetime(df[delivery_col], errors="coerce")
                delivery_days = (delivery_dates - order_dates).dt.days
                avg_delivery = delivery_days.mean()
            except Exception:
                avg_delivery = 0

        # Regional
        if region_col and revenue_col:
            top_region = df.groupby(region_col)[revenue_col].sum().idxmax()
            top_region_revenue = df.groupby(region_col)[revenue_col].sum().max()
        else:
            top_region = "N/A"
            top_region_revenue = 0

        summary = f"""
==================================================
EXECUTIVE BUSINESS SUMMARY
==================================================

REVENUE PERFORMANCE
-------------------
Total Revenue: ${total_revenue:,.2f}
Average Order Value: ${aov:,.2f}
Total Customers: {total_customers:,}

PRODUCT PERFORMANCE
-------------------
Top Category: {top_category}
Top Category Revenue: ${top_category_revenue:,.2f}

REGIONAL PERFORMANCE
-------------------
Top Region: {top_region}
Top Region Revenue: ${top_region_revenue:,.2f}

CUSTOMER ANALYSIS
-------------------
Total Unique Customers: {total_customers:,}

DELIVERY PERFORMANCE
-------------------
Average Delivery Days: {avg_delivery:.1f}

==================================================
END OF REPORT
==================================================
"""
        return summary

    # SQL mode (legacy) — no arguments
    summary = f"""
==================================================
EXECUTIVE BUSINESS SUMMARY
==================================================

REVENUE PERFORMANCE
-------------------
{revenue_summary()}

PRODUCT PERFORMANCE
-------------------
{product_summary()}

REGIONAL PERFORMANCE
-------------------
{regional_summary()}

CUSTOMER ANALYSIS
-------------------
{customer_summary()}

DELIVERY PERFORMANCE
-------------------
{delivery_summary()}

==================================================
END OF REPORT
==================================================
"""
    return summary