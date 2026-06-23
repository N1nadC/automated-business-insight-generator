import pandas as pd


def load_raw_data():
    datasets = {
        "customers": pd.read_csv("data/raw/olist_customers_dataset.csv"),
        "orders": pd.read_csv("data/raw/olist_orders_dataset.csv"),
        "order_items": pd.read_csv("data/raw/olist_order_items_dataset.csv"),
        "products": pd.read_csv("data/raw/olist_products_dataset.csv"),
        "payments": pd.read_csv("data/raw/olist_order_payments_dataset.csv"),
        "reviews": pd.read_csv("data/raw/olist_order_reviews_dataset.csv"),
        "locations": pd.read_csv("data/raw/olist_geolocation_dataset.csv"),
        "translation": pd.read_csv(
            "data/raw/product_category_name_translation.csv"
        )
    }

    return datasets