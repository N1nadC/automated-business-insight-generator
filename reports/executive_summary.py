from insights.revenue_insights import revenue_summary
from insights.product_insights import product_summary
from insights.regional_insights import regional_summary
from insights.customer_insights import customer_summary
from insights.delivery_insights import delivery_summary


def generate_executive_summary():

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