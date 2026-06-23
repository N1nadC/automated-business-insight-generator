from utils.query_runner import run_query


def get_top_products(limit=10):

    query = f"""
    SELECT
        oi.product_id,
        ROUND(SUM(oi.price)::numeric,2) AS revenue
    FROM order_items oi
    GROUP BY oi.product_id
    ORDER BY revenue DESC
    LIMIT {limit}
    """

    return run_query(query)

def category_performance():

    query = """
    SELECT
        p.product_category_name_english,
        ROUND(SUM(oi.price)::numeric,2) AS revenue
    FROM order_items oi
    JOIN products p
      ON oi.product_id=p.product_id
    GROUP BY p.product_category_name_english
    ORDER BY revenue DESC
    """

    return run_query(query)
