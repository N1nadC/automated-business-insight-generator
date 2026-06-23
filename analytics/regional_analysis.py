from utils.query_runner import run_query


def revenue_by_state():

    query = """
    SELECT
        c.customer_state,
        ROUND(SUM(p.payment_value)::numeric,2) AS revenue
    FROM customers c
    JOIN orders o
      ON c.customer_id=o.customer_id
    JOIN payments p
      ON o.order_id=p.order_id
    GROUP BY customer_state
    ORDER BY revenue DESC
    """

    return run_query(query)
