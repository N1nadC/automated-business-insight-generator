from pathlib import Path
import pandas as pd
from database.db_connection import engine

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

tables = {
    "customers": PROCESSED_DIR / "customers.csv",
    "orders": PROCESSED_DIR / "orders.csv",
    "order_items": PROCESSED_DIR / "order_items.csv",
    "products": PROCESSED_DIR / "products.csv",
    "payments": PROCESSED_DIR / "payments.csv",
    "reviews": PROCESSED_DIR / "reviews.csv",
    "locations": PROCESSED_DIR / "locations.csv"
}

for table_name, file_path in tables.items():

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"{table_name} loaded successfully")

print("\nAll tables loaded successfully.")