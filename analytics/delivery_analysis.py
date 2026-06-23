from utils.query_runner import run_query


from utils.query_runner import run_query


def average_delivery_days():

    query = """
    SELECT
    AVG(
        DATE_PART(
            'day',
            CAST(o.order_delivered_customer_date AS timestamp)
            -
            CAST(o.order_purchase_timestamp AS timestamp)
        )
    ) AS avg_delivery_days
    FROM orders o
    WHERE o.order_delivered_customer_date IS NOT NULL
    AND o.order_purchase_timestamp IS NOT NULL
    AND o.order_status='delivered'
    """

    df = run_query(query)

    return float(df.iloc[0,0])
