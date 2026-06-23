from analytics.delivery_analysis import average_delivery_days


def delivery_summary():

    days = days = average_delivery_days()

    return (
    f"The average delivery time was {days:.2f} days, "
    f"indicating stable logistics performance."
    )