import pandas as pd


def process_data(datasets):

    customers = datasets["customers"]
    orders = datasets["orders"]
    order_items = datasets["order_items"]
    products = datasets["products"]
    payments = datasets["payments"]
    reviews = datasets["reviews"]
    locations = datasets["locations"]
    translation = datasets["translation"]

    # Remove duplicates
    customers = customers.drop_duplicates()
    orders = orders.drop_duplicates()
    order_items = order_items.drop_duplicates()
    products = products.drop_duplicates()
    payments = payments.drop_duplicates()
    reviews = reviews.drop_duplicates()

    # Merge product translation
    products = products.merge(
        translation,
        on="product_category_name",
        how="left"
    )

    return {
        "customers": customers,
        "orders": orders,
        "order_items": order_items,
        "products": products,
        "payments": payments,
        "reviews": reviews,
        "locations": locations
    }