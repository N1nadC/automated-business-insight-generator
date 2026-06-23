from utils.query_runner import run_query


def get_total_revenue():

    query = """
    SELECT
        ROUND(SUM(payment_value)::numeric,2) AS total_revenue
    FROM payments
    """

    return run_query(query)

def get_average_order_value():

    query = """
    SELECT
        ROUND(AVG(payment_value)::numeric,2) AS avg_order_value
    FROM payments
    """

    return run_query(query)
