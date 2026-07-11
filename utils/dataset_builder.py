import pandas as pd


def build_business_dataset():

    # Load datasets
    customers = pd.read_csv("data/processed/customers.csv")
    orders = pd.read_csv("data/processed/orders.csv")
    order_items = pd.read_csv("data/processed/order_items.csv")
    products = pd.read_csv("data/processed/products.csv")
    payments = pd.read_csv("data/processed/payments.csv")
    # locations = pd.read_csv("data/processed/locations.csv")

    # -----------------------------
    # Merge Customers + Orders
    # -----------------------------
    df = orders.merge(
        customers,
        on="customer_id",
        how="left"
    )

    # -----------------------------
    # Merge Order Items
    # -----------------------------
    df = df.merge(
        order_items,
        on="order_id",
        how="left"
    )

    # -----------------------------
    # Merge Products
    # -----------------------------
    df = df.merge(
        products,
        on="product_id",
        how="left"
    )

    # -----------------------------
    # Merge Payments
    # -----------------------------
    df = df.merge(
        payments,
        on="order_id",
        how="left"
    )

    # # -----------------------------
    # # Merge Locations (optional)
    # # -----------------------------
    # if "customer_zip_code_prefix" in df.columns:
    #     df = df.merge(
    #         locations,
    #         left_on="customer_zip_code_prefix",
    #         right_on="geolocation_zip_code_prefix",
    #         how="left"
    #     )

    return df