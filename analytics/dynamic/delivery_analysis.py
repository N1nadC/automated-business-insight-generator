import pandas as pd


def get_average_delivery_days(df, schema):
    """
    Calculate average delivery time in days.
    """

    purchase_col = schema.get("date")
    delivery_col = schema.get("delivery")

    if purchase_col is None:
        raise ValueError("Purchase date column not detected.")

    if delivery_col is None:
        raise ValueError("Delivery date column not detected.")

    temp = df.copy()

    temp[purchase_col] = pd.to_datetime(
        temp[purchase_col],
        errors="coerce"
    )

    temp[delivery_col] = pd.to_datetime(
        temp[delivery_col],
        errors="coerce"
    )

    temp["delivery_days"] = (
        temp[delivery_col] - temp[purchase_col]
    ).dt.days

    temp = temp.dropna(subset=["delivery_days"])

    return float(temp["delivery_days"].mean())


def get_delivery_statistics(df, schema):
    """
    Returns delivery KPIs.
    """

    purchase_col = schema.get("date")
    delivery_col = schema.get("delivery")

    temp = df.copy()

    temp[purchase_col] = pd.to_datetime(
        temp[purchase_col],
        errors="coerce"
    )

    temp[delivery_col] = pd.to_datetime(
        temp[delivery_col],
        errors="coerce"
    )

    temp["delivery_days"] = (
        temp[delivery_col] - temp[purchase_col]
    ).dt.days

    temp = temp.dropna(subset=["delivery_days"])

    return {
        "average_delivery_days": float(temp["delivery_days"].mean()),
        "minimum_delivery_days": float(temp["delivery_days"].min()),
        "maximum_delivery_days": float(temp["delivery_days"].max())
    }