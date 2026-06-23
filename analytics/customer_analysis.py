from utils.query_runner import run_query


def total_customers():
    """
    Returns the total number of customers.

    Returns
    -------
    int
        Total count of customers in the database.
    """
    query = """
    SELECT COUNT(*) AS customers
    FROM customers
    """

    df = run_query(query)
    return int(df.iloc[0, 0])


def top_customer_states():
    """
    Returns customer count grouped by state.

    Returns
    -------
    pandas.DataFrame
        Columns: customer_state, customers
    """
    query = """
    SELECT
        customer_state,
        COUNT(*) AS customers
    FROM customers
    GROUP BY customer_state
    ORDER BY customers DESC
    """

    return run_query(query)
