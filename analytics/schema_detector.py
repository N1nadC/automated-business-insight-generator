"""
Schema Detection Engine

This module automatically detects important business columns
from a cleaned dataset.

The detected schema is used by the analytics engine,
visualizations, KPI engine, and insight generation engine.
"""


def detect_schema(df):
    """
    Detect important business columns from a dataset.

    Returns
    -------
    dict
        Example:
        {
            "revenue": "payment_value",
            "date": "order_purchase_timestamp",
            "customer": "customer_id",
            "product": "product_id",
            "category": "product_category_name_english",
            "region": "customer_state",
            "delivery": "order_delivered_customer_date"
            
        }
    """

    columns = {col.lower().strip(): col for col in df.columns}

    aliases = {
        "revenue": [
            "payment_value",
            "revenue",
            "sales",
            "amount",
            "price",
            "total_sales",
            "gross_sales",
            "net_sales"
        ],


        "date": [
            "date",
            "order date",
            "order_date",
            "purchase date",
            "purchase_date",
            "invoice date",
            "invoice_date",
            "transaction date",
            "transaction_date",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_customer_date",
            "order_delivered_carrier_date",
            "order_estimated_delivery_date"
        ],

        "customer": [
            "customer",
            "customer id",
            "customer_id",
            "client",
            "client id",
            "client_id"
        ],

        "product": [
            "product",
            "product id",
            "product_id",
            "product name"
        ],

        "category": [
            "category",
            "product category",
            "subcategory",
            "product_category_name_english",
            "product_category_name",
            "product_category"
        ],

        "region": [
            "region",
            "state",
            "city",
            "country",
            "province",
            "customer_state",
        ],

        "delivery": [
            "order_delivered_customer_date",
            "delivery_date",
            "delivery_days",
            "delivery time",
            "delivery_time",
            "shipping_days"
        ]
    }

    schema = {}

    for field, possible_names in aliases.items():

        schema[field] = None

        for alias in possible_names:

            if alias in columns:
                schema[field] = columns[alias]
                break

    return schema


def get_missing_required_fields(schema):
    """
    Returns a list of missing mandatory fields.
    """

    required = [
        "revenue",
        "date"
    ]

    missing = []

    for field in required:

        if schema[field] is None:
            missing.append(field)

    return missing


def is_schema_valid(schema):
    """
    Returns True if the uploaded dataset
    contains the minimum required fields.
    """

    return len(get_missing_required_fields(schema)) == 0


def print_schema(schema):
    """
    Pretty-print detected schema.
    """

    print("\nDetected Schema")
    print("-" * 40)

    for key, value in schema.items():

        if value is None:
            print(f"{key:<12}: Not Found")

        else:
            print(f"{key:<12}: {value}")