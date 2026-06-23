from analytics.regional_analysis import revenue_by_state


def regional_summary():

    df = revenue_by_state()

    state = df.iloc[0]["customer_state"]
    revenue = df.iloc[0]["revenue"]

    total_revenue = df["revenue"].sum()
    contribution = revenue / total_revenue * 100

    insight = (
        f"State {state} contributed ${revenue:,.2f}, "
        f"representing {contribution:.1f}% of total revenue."
    )

    return insight