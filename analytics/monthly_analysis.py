from utils.query_runner import run_query


def get_monthly_sales():

    query = """
    SELECT
        DATE_TRUNC('month', o.order_purchase_timestamp::timestamp) AS month,
        ROUND(SUM(p.payment_value)::numeric,2) AS revenue
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY month
    ORDER BY month
    """

    return run_query(query)
