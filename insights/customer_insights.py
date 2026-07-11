import pandas as pd
import numpy as np

from analytics.dynamic.customer_analysis import (
    get_total_customers
)


def customer_summary(df=None, schema=None):
    """
    Legacy simple customer summary for reports.executive_summary compatibility.
    """
    if df is not None and schema is not None:
        customers = get_total_customers(df, schema)
        return (
            f"The dataset contains "
            f"{customers:,} unique customers."
        )
    return "Customer data not available."


def analyze_customer_behavior(df, schema):
    """
    Deep customer analysis with segmentation, loyalty metrics,
    churn risk indicators, and acquisition insights.
    """
    customer_col = schema.get("customer")
    revenue_col = schema.get("revenue")
    date_col = schema.get("date")
    region_col = schema.get("region")

    if not customer_col:
        return {"error": "Customer column not detected"}

    insights = {
        "findings": [],
        "recommendations": [],
        "risks": [],
        "opportunities": []
    }

    # ── Basic Metrics ──
    total_customers = df[customer_col].nunique()
    insights["total_customers"] = int(total_customers)
    insights["findings"].append(f"👥 Total unique customers: {total_customers:,}")

    if revenue_col:
        df[revenue_col] = pd.to_numeric(df[revenue_col], errors="coerce")

        # Customer lifetime value distribution
        clv = df.groupby(customer_col)[revenue_col].sum()
        insights["avg_clv"] = float(clv.mean())
        insights["median_clv"] = float(clv.median())
        insights["max_clv"] = float(clv.max())

        # CLV distribution analysis
        q75, q95 = clv.quantile([0.75, 0.95])
        top_5_pct = (clv >= q95).sum() / total_customers * 100
        top_25_pct = (clv >= q75).sum() / total_customers * 100

        insights["findings"].append(f"💰 Avg Customer Lifetime Value: ${insights['avg_clv']:,.2f}")
        insights["findings"].append(f"📊 CLV Distribution: Top 5% of customers ({top_5_pct:.1f}%) drive disproportionate value. Top 25%: {top_25_pct:.1f}%")

        if top_5_pct > 15:
            insights["risks"].append("CUSTOMER CONCENTRATION: Top 5% represent too large a share. Losing even a few would hurt significantly.")
            insights["recommendations"].append("Implement VIP retention program for top 5%. Dedicated account management and exclusive perks.")
        else:
            insights["opportunities"].append("Healthy customer distribution. Focus on moving mid-tier customers to high-tier via upselling.")

        # Order frequency analysis
        order_counts = df.groupby(customer_col).size()
        insights["avg_orders_per_customer"] = float(order_counts.mean())
        insights["repeat_customer_rate"] = round((order_counts > 1).sum() / total_customers * 100, 1)

        insights["findings"].append(f"🔄 Repeat Purchase Rate: {insights['repeat_customer_rate']:.1f}% ({(order_counts > 1).sum():,} of {total_customers:,} customers)")
        insights["findings"].append(f"📦 Avg Orders per Customer: {insights['avg_orders_per_customer']:.1f}")

        if insights["repeat_customer_rate"] < 20:
            insights["risks"].append("LOW LOYALTY: Most customers are one-time buyers. High acquisition cost, low lifetime value.")
            insights["recommendations"].append("CRITICAL: Launch retention program. Post-purchase email sequences, loyalty points, subscription models.")
            insights["recommendations"].append("Analyze why customers don't return — product satisfaction, delivery experience, or follow-up gaps?")
        elif insights["repeat_customer_rate"] < 40:
            insights["findings"].append(f"⚠️ Moderate loyalty. {100 - insights['repeat_customer_rate']:.1f}% of customers never return.")
            insights["recommendations"].append("Improve onboarding experience. First 30 days are critical for retention.")
        else:
            insights["findings"].append(f"✅ Strong loyalty base. {insights['repeat_customer_rate']:.1f}% of customers are repeat buyers.")
            insights["opportunities"].append("Leverage loyal customers for referrals. Implement advocacy program with incentives.")

        # One-time buyer analysis
        one_time = (order_counts == 1).sum()
        one_time_revenue = clv[order_counts == 1].sum()
        one_time_share = one_time_revenue / clv.sum() * 100

        insights["findings"].append(f"💸 One-time buyers: {one_time:,} customers contributing only {one_time_share:.1f}% of total revenue.")

        if one_time > total_customers * 0.6:
            insights["recommendations"].append(f"{one_time:,} one-time buyers represent untapped potential. Targeted win-back campaigns could yield significant returns.")

    # ── Regional Customer Distribution ──
    if region_col:
        region_customers = df.groupby(region_col)[customer_col].nunique().sort_values(ascending=False)
        top_region = region_customers.index[0]
        top_region_count = int(region_customers.iloc[0])
        top_region_share = top_region_count / total_customers * 100

        insights["findings"].append(f"🌍 Geographic Concentration: {top_region_share:.1f}% of customers are in {top_region} ({top_region_count:,})")

        if top_region_share > 50:
            insights["risks"].append(f"GEOGRAPHIC RISK: {top_region_share:.1f}% customer concentration in {top_region}. Regional economic downturn would devastate revenue.")
            insights["recommendations"].append(f"URGENT: Diversify geographically. Target underpenetrated regions: {', '.join(region_customers.tail(3).index.tolist())}")
        elif top_region_share > 30:
            insights["recommendations"].append(f"Expand in secondary regions. {region_customers.index[1]} and {region_customers.index[2]} show growth potential.")
        else:
            insights["opportunities"].append("Well-distributed customer base. Test localized marketing in mid-tier regions.")

        # Untapped regions
        if len(region_customers) > 5:
            small_regions = region_customers[region_customers < region_customers.mean() * 0.5]
            if len(small_regions) > 0:
                insights["opportunities"].append(f"Untapped markets: {', '.join(small_regions.index[:3].tolist())} — consider pilot programs with localized offerings.")

    # ── Recency Analysis (if date available) ──
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        latest_date = df[date_col].max()

        customer_recency = df.groupby(customer_col)[date_col].max()
        days_since = (latest_date - customer_recency).dt.days

        # RFM-style recency segments
        recent = (days_since <= 30).sum()
        at_risk = ((days_since > 30) & (days_since <= 90)).sum()
        dormant = (days_since > 90).sum()

        insights["findings"].append(f"⏰ Customer Recency (as of {latest_date.strftime('%Y-%m-%d')}):")
        insights["findings"].append(f"   🟢 Active (≤30 days): {recent:,} ({recent/total_customers*100:.1f}%)")
        insights["findings"].append(f"   🟡 At Risk (31-90 days): {at_risk:,} ({at_risk/total_customers*100:.1f}%)")
        insights["findings"].append(f"   🔴 Dormant (>90 days): {dormant:,} ({dormant/total_customers*100:.1f}%)")

        if dormant > total_customers * 0.3:
            insights["risks"].append(f"CHURN CRISIS: {dormant:,} customers dormant >90 days. Massive reactivation opportunity or systemic issue.")
            insights["recommendations"].append(f"Launch aggressive win-back campaign for {dormant:,} dormant customers. Special discounts + personalized outreach.")
        elif at_risk > total_customers * 0.3:
            insights["recommendations"].append(f"{at_risk:,} customers at risk of churning. Preventive retention campaign before they go dormant.")
        else:
            insights["opportunities"].append(f"Healthy active base. Use {recent:,} recent customers for referral programs and reviews.")

    return insights


def generate_customer_insights_text(df, schema):
    """Generate formatted text insights for display."""
    analysis = analyze_customer_behavior(df, schema)

    if "error" in analysis:
        return f"⚠️ {analysis['error']}"

    lines = [
        "=" * 60,
        "👥 CUSTOMER INTELLIGENCE REPORT",
        "=" * 60,
        "",
        f"👥 Total Customers: {analysis['total_customers']:,}",
    ]

    if "avg_clv" in analysis:
        lines.extend([
            f"💰 Avg CLV: ${analysis['avg_clv']:,.2f}",
            f"📊 Median CLV: ${analysis['median_clv']:,.2f}",
            f"🏆 Max CLV: ${analysis['max_clv']:,.2f}",
            f"🔄 Repeat Rate: {analysis['repeat_customer_rate']:.1f}%",
            f"📦 Avg Orders/Customer: {analysis['avg_orders_per_customer']:.1f}",
        ])

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
