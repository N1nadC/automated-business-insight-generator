import pandas as pd
import numpy as np

from analytics.dynamic.delivery_analysis import (
    get_average_delivery_days
)


def delivery_summary(df=None, schema=None):
    """
    Legacy simple delivery summary for reports.executive_summary compatibility.
    """
    if df is not None and schema is not None:
        days = get_average_delivery_days(df, schema)
        return (
            f"The average delivery time "
            f"was {days:.2f} days."
        )
    return "Delivery data not available."


def analyze_delivery_performance(df, schema):
    """
    Deep delivery analysis with SLA compliance, bottleneck identification,
    cost impact, and operational recommendations.
    """
    delivery_col = schema.get("delivery")
    date_col = schema.get("date")
    revenue_col = schema.get("revenue")
    region_col = schema.get("region")
    customer_col = schema.get("customer")

    if not delivery_col or not date_col:
        return {"error": "Delivery or date column not detected"}

    insights = {
        "findings": [],
        "recommendations": [],
        "risks": [],
        "opportunities": []
    }

    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df[delivery_col] = pd.to_datetime(df[delivery_col], errors="coerce")
    df["delivery_days"] = (df[delivery_col] - df[date_col]).dt.days

    # Clean data
    df = df[df["delivery_days"] >= 0]  # Remove negative (data errors)

    avg_days = df["delivery_days"].mean()
    median_days = df["delivery_days"].median()
    std_days = df["delivery_days"].std()
    max_days = df["delivery_days"].max()
    min_days = df["delivery_days"].min()

    insights["avg_days"] = round(avg_days, 1)
    insights["median_days"] = round(median_days, 1)
    insights["std_days"] = round(std_days, 1)
    insights["max_days"] = int(max_days)
    insights["min_days"] = int(min_days)

    insights["findings"].append(f"🚚 Average Delivery: {avg_days:.1f} days (Median: {median_days:.1f})")
    insights["findings"].append(f"📊 Delivery Range: {min_days} to {max_days} days (Std: {std_days:.1f})")

    # SLA Analysis
    sla_targets = [3, 5, 7, 10, 14]
    for sla in sla_targets:
        pct = (df["delivery_days"] <= sla).mean() * 100
        insights[f"sla_{sla}day"] = round(pct, 1)

    insights["findings"].append(f"⏱️ SLA Performance:")
    insights["findings"].append(f"   ≤3 days: {insights['sla_3day']:.1f}% | ≤5 days: {insights['sla_5day']:.1f}% | ≤7 days: {insights['sla_7day']:.1f}%")
    insights["findings"].append(f"   ≤10 days: {insights['sla_10day']:.1f}% | ≤14 days: {insights['sla_14day']:.1f}%")

    if insights["sla_7day"] < 50:
        insights["risks"].append(f"CRITICAL SLA FAILURE: Only {insights['sla_7day']:.1f}% of orders delivered within 7 days. Industry standard is 70%+.")
        insights["recommendations"].append("URGENT: Complete logistics overhaul. Evaluate 3PL partners, regional warehouses, or dropshipping models.")
    elif insights["sla_7day"] < 70:
        insights["risks"].append(f"SLA WARNING: {insights['sla_7day']:.1f}% within 7 days. Below competitive threshold.")
        insights["recommendations"].append("Priority: Optimize fulfillment process. Identify bottlenecks in pick-pack-ship workflow.")
    else:
        insights["opportunities"].append(f"✅ Strong delivery performance ({insights['sla_7day']:.1f}% within 7 days). Market this as a competitive advantage.")

    # Extreme delays
    extreme_delays = (df["delivery_days"] > 30).sum()
    if extreme_delays > 0:
        extreme_pct = extreme_delays / len(df) * 100
        insights["findings"].append(f"🚨 Extreme Delays: {extreme_delays:,} orders ({extreme_pct:.1f}%) took >30 days")
        insights["risks"].append(f"{extreme_delays:,} customers experienced >30 day delivery. Expect high churn and negative reviews.")
        insights["recommendations"].append(f"Immediate: Contact {extreme_delays:,} delayed customers with apologies + compensation. Review carrier contracts.")

    # Consistency analysis
    if std_days > avg_days * 0.5:
        insights["findings"].append(f"⚠️ High delivery variability (CV: {std_days/avg_days*100:.1f}%). Unpredictable experience damages trust.")
        insights["recommendations"].append("Standardize processes. High variability suggests inconsistent carrier performance or warehouse operations.")
    else:
        insights["findings"].append(f"✅ Consistent delivery (CV: {std_days/avg_days*100:.1f}%). Reliable experience builds customer loyalty.")

    # Revenue impact of delivery
    if revenue_col:
        df[revenue_col] = pd.to_numeric(df[revenue_col], errors="coerce")

        # Compare revenue: fast vs slow delivery
        fast_orders = df[df["delivery_days"] <= median_days]
        slow_orders = df[df["delivery_days"] > median_days]

        if len(fast_orders) > 0 and len(slow_orders) > 0:
            fast_avg_revenue = fast_orders[revenue_col].mean()
            slow_avg_revenue = slow_orders[revenue_col].mean()
            revenue_impact = (fast_avg_revenue - slow_avg_revenue) / slow_avg_revenue * 100 if slow_avg_revenue > 0 else 0

            insights["findings"].append(f"💰 Delivery-Revenue Correlation:")
            insights["findings"].append(f"   Fast delivery (≤{median_days:.0f}d) avg order: ${fast_avg_revenue:.2f}")
            insights["findings"].append(f"   Slow delivery (>{median_days:.0f}d) avg order: ${slow_avg_revenue:.2f}")

            if revenue_impact > 10:
                insights["opportunities"].append(f"FAST DELIVERY PREMIUM: Orders with fast delivery are worth {revenue_impact:.1f}% more. Customers willing to pay for speed — offer expedited shipping tiers.")
            elif revenue_impact < -10:
                insights["risks"].append(f"SLOW DELIVERY PENALTY: Slow orders are {abs(revenue_impact):.1f}% lower value. Delayed customers reduce order size or cancel.")
                insights["recommendations"].append("Incentivize faster delivery — free expedited shipping for orders >$X to offset revenue loss.")

    # Regional delivery analysis
    if region_col:
        region_delivery = df.groupby(region_col)["delivery_days"].agg(['mean', 'std', 'count']).round(1)
        region_delivery = region_delivery.sort_values("mean")

        insights["findings"].append(f"🌍 Best Delivery Region: {region_delivery.index[0]} ({region_delivery.iloc[0]['mean']:.1f} days, {region_delivery.iloc[0]['count']:,} orders)")
        insights["findings"].append(f"🐌 Worst Delivery Region: {region_delivery.index[-1]} ({region_delivery.iloc[-1]['mean']:.1f} days, {region_delivery.iloc[-1]['count']:,} orders)")

        worst_region = region_delivery.index[-1]
        worst_avg = region_delivery.iloc[-1]['mean']
        if worst_avg > avg_days * 1.5:
            insights["risks"].append(f"REGIONAL DELIVERY CRISIS: {worst_region} averages {worst_avg:.1f} days — {worst_avg/avg_days:.1f}x worse than company average.")
            insights["recommendations"].append(f"Priority logistics investment in {worst_region}. Local warehouse or regional carrier partnership needed.")

    # Customer satisfaction proxy (repeat rate by delivery speed)
    if customer_col:
        customer_orders = df.groupby(customer_col).agg({
            "delivery_days": "mean",
            customer_col: "size"
        }).rename(columns={customer_col: "order_count"})

        fast_customers = customer_orders[customer_orders["delivery_days"] <= median_days]
        slow_customers = customer_orders[customer_orders["delivery_days"] > median_days]

        fast_repeat = (fast_customers["order_count"] > 1).mean() * 100
        slow_repeat = (slow_customers["order_count"] > 1).mean() * 100

        insights["findings"].append(f"🔄 Repeat Purchase Rate:")
        insights["findings"].append(f"   Fast delivery customers: {fast_repeat:.1f}% repeat")
        insights["findings"].append(f"   Slow delivery customers: {slow_repeat:.1f}% repeat")

        repeat_gap = fast_repeat - slow_repeat
        if repeat_gap > 15:
            insights["opportunities"].append(f"DELIVERY DRIVES LOYALTY: {repeat_gap:.1f} percentage point higher repeat rate for fast-delivery customers. Every day faster = retention gold.")
            insights["recommendations"].append("Quantify delivery ROI: Calculate lifetime value difference between fast/slow delivery cohorts. Use for logistics budget justification.")
        elif repeat_gap < -5:
            insights["risks"].append(f"ALARMING: Slow delivery customers actually repeat more. Investigate — possible data artifact or different customer segment behavior.")

    return insights


def generate_delivery_insights_text(df, schema):
    """Generate formatted text insights for display."""
    analysis = analyze_delivery_performance(df, schema)

    if "error" in analysis:
        return f"⚠️ {analysis['error']}"

    lines = [
        "=" * 60,
        "🚚 DELIVERY INTELLIGENCE REPORT",
        "=" * 60,
        "",
        f"📊 Average Delivery: {analysis['avg_days']:.1f} days",
        f"📊 Median Delivery: {analysis['median_days']:.1f} days",
        f"📊 Std Deviation: {analysis['std_days']:.1f} days",
        f"📊 Range: {analysis['min_days']} - {analysis['max_days']} days",
        "",
        f"⏱️ SLA Performance:",
        f"   ≤3 days: {analysis['sla_3day']:.1f}%",
        f"   ≤5 days: {analysis['sla_5day']:.1f}%",
        f"   ≤7 days: {analysis['sla_7day']:.1f}%",
        f"   ≤10 days: {analysis['sla_10day']:.1f}%",
        f"   ≤14 days: {analysis['sla_14day']:.1f}%",
    ]

    lines.extend(["", "🔍 KEY FINDINGS", "-" * 40])
    for finding in analysis["findings"]:
        lines.append(f"  • {finding}")

    if analysis["recommendations"]:
        lines.extend(["", "💡 RECOMMENDATIONS", "-" * 40])
        for rec in analysis["recommendations"]:
            lines.append(f"  → {rec}")

    if analysis["risks"]:
        lines.extend(["", "🚨 RISK FLAGS", "-" * 40])
        for risk in analysis["risks"]:
            lines.append(f"  ⚠️ {risk}")

    if analysis["opportunities"]:
        lines.extend(["", "🎯 OPPORTUNITIES", "-" * 40])
        for opp in analysis["opportunities"]:
            lines.append(f"  ⭐ {opp}")

    lines.extend(["", "=" * 60])
    return "\n".join(lines)
