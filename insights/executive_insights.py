from insights.revenue_insights import revenue_summary
from insights.product_insights import top_category_insight
from insights.regional_insights import regional_summary
from insights.customer_insights import customer_summary
from insights.delivery_insights import delivery_summary


def executive_summary():

    return [
        revenue_summary(),
        top_category_insight(),
        regional_summary(),
        customer_summary(),
        delivery_summary()
    ]