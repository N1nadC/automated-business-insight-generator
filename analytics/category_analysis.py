from utils.query_runner import run_query


def category_performance():
    query = """
    SELECT
        p.product_category_name_english,
        SUM(oi.price) AS revenue
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY p.product_category_name_english
    ORDER BY revenue DESC
    """

    return run_query(query)