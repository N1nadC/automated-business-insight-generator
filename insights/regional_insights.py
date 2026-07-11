import pandas as pd
import numpy as np

from analytics.dynamic.regional_analysis import (
    get_top_region
)


def regional_summary(df=None, schema=None):
    """
    Legacy simple regional summary for reports.executive_summary compatibility.
    """
    if df is not None and schema is not None:
        top = get_top_region(df, schema)
        return (
            f"The highest revenue was generated in "
            f"'{top['region']}', contributing "
            f"${top['revenue']:,.2f}."
        )
    return "Regional data not available."


def analyze_regional_performance(df, schema):
    """
    Deep regional analysis with market penetration, growth potential,
    delivery efficiency by region, and expansion recommendations.
    """
    region_col = schema.get("region")
    revenue_col = schema.get("revenue")
    customer_col = schema.get("customer")
    delivery_col = schema.get("delivery")
    date_col = schema.get("date")

    if not region_col:
        return {"error": "Region column not detected"}

    insights = {
        "findings": [],
        "recommendations": [],
        "risks": [],
        "opportunities": []
    }

    # ── Revenue by Region ──
    if revenue_col:
        df[revenue_col] = pd.to_numeric(df[revenue_col], errors="coerce")
        regional_revenue = df.groupby(region_col)[revenue_col].sum().sort_values(ascending=False)
        total_revenue = regional_revenue.sum()

        insights["top_region"] = regional_revenue.index[0]
        insights["top_region_revenue"] = float(regional_revenue.iloc[0])
        insights["top_region_share"] = round(regional_revenue.iloc[0] / total_revenue * 100, 1)
        insights["region_count"] = len(regional_revenue)

        # Market concentration
        top_3_share = regional_revenue.head(3).sum() / total_revenue * 100
        insights["findings"].append(f"🌍 Top 3 regions control {top_3_share:.1f}% of total revenue.")
        insights["findings"].append(f"🏆 {insights['top_region']} leads with ${insights['top_region_revenue']:,.2f} ({insights['top_region_share']}%)")

        if top_3_share > 80:
            insights["risks"].append(f"EXTREME GEOGRAPHIC CONCENTRATION: Top 3 regions = {top_3_share:.1f}%. Economic/political events in these regions are existential threats.")
            insights["recommendations"].append("CRITICAL: Aggressive expansion into untapped regions. Consider partnerships or acquisitions to establish presence quickly.")
        elif top_3_share > 60:
            insights["findings"].append(f"⚠️ Significant concentration in top 3 regions ({top_3_share:.1f}%).")
            insights["recommendations"].append("Diversify revenue geographically. Identify 2-3 secondary regions for targeted growth campaigns.")
        else:
            insights["opportunities"].append("Balanced regional distribution. Leverage this stability to test new markets with lower risk.")

        # Bottom performers
        bottom_3 = regional_revenue.tail(3)
        insights["findings"].append(f"📉 Bottom 3 regions: {', '.join(bottom_3.index.tolist())} — combined ${bottom_3.sum():,.2f}")

        # Growth opportunity score (revenue per region vs. avg)
        avg_revenue = regional_revenue.mean()
        underperformers = regional_revenue[regional_revenue < avg_revenue * 0.5]
        if len(underperformers) > 0:
            insights["opportunities"].append(f"HIGH POTENTIAL: {len(underperformers)} regions underperforming vs. average. Targeted investment could yield 2-3x returns: {', '.join(underperformers.index[:3].tolist())}")

        # Revenue per customer by region (efficiency metric)
        if customer_col:
            region_customers = df.groupby(region_col)[customer_col].nunique()
            rpc = regional_revenue / region_customers
            rpc_sorted = rpc.sort_values(ascending=False)

            insights["findings"].append(f"💰 Revenue per Customer leader: {rpc_sorted.index[0]} (${rpc_sorted.iloc[0]:,.2f}/customer)")
            insights["findings"].append(f"📊 Revenue per Customer laggard: {rpc_sorted.index[-1]} (${rpc_sorted.iloc[-1]:,.2f}/customer)")

            rpc_gap = rpc_sorted.iloc[0] / rpc_sorted.iloc[-1] if rpc_sorted.iloc[-1] > 0 else float('inf')
            if rpc_gap > 3:
                insights["opportunities"].append(f"MASSIVE EFFICIENCY GAP: {rpc_gap:.1f}x difference in revenue per customer between best and worst regions. Replicate {rpc_sorted.index[0]}'s strategy in {rpc_sorted.index[-1]}.")
                insights["recommendations"].append(f"Study {rpc_sorted.index[0]}'s playbook — pricing, product mix, marketing channels. Apply learnings to {rpc_sorted.index[-1]} and similar underperformers.")

    # ── Customer Distribution ──
    if customer_col:
        region_customers = df.groupby(region_col)[customer_col].nunique().sort_values(ascending=False)
        total_customers = region_customers.sum()

        insights["findings"].append(f"👥 Customer distribution: {region_customers.index[0]} leads with {region_customers.iloc[0]:,} customers ({region_customers.iloc[0]/total_customers*100:.1f}%)")

        # Penetration opportunity
        if revenue_col:
            revenue_per_customer = regional_revenue / region_customers
            low_penetration = revenue_per_customer[revenue_per_customer < revenue_per_customer.mean() * 0.7]
            if len(low_penetration) > 0:
                insights["opportunities"].append(f"PENETRATION GAP: {len(low_penetration)} regions have high customer counts but low revenue per customer. Upselling opportunity: {', '.join(low_penetration.index[:3].tolist())}")

    # ── Delivery Performance by Region ──
    if delivery_col and revenue_col:
        df[delivery_col] = pd.to_datetime(df[delivery_col], errors="coerce")
        if date_col:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            df["delivery_days"] = (df[delivery_col] - df[date_col]).dt.days

            region_delivery = df.groupby(region_col)["delivery_days"].mean().sort_values()

            insights["findings"].append(f"🚚 Fastest delivery: {region_delivery.index[0]} ({region_delivery.iloc[0]:.1f} days avg)")
            insights["findings"].append(f"🐌 Slowest delivery: {region_delivery.index[-1]} ({region_delivery.iloc[-1]:.1f} days avg)")

            delivery_gap = region_delivery.iloc[-1] - region_delivery.iloc[0]
            if delivery_gap > 10:
                insights["risks"].append(f"DELIVERY INEQUITY: {delivery_gap:.1f} day gap between fastest and slowest regions. Customers in {region_delivery.index[-1]} receiving inferior service.")
                insights["recommendations"].append(f"URGENT: Logistics audit for {region_delivery.index[-1]}. Consider regional fulfillment centers or local delivery partners.")

            # Correlation: delivery speed vs revenue
            merged = pd.DataFrame({
                "delivery_days": region_delivery,
                "revenue": regional_revenue
            }).dropna()
            if len(merged) > 3:
                corr = merged["delivery_days"].corr(merged["revenue"])
                if abs(corr) > 0.5:
                    direction = "faster" if corr < 0 else "slower"
                    insights["findings"].append(f"📈 Strong correlation: {direction} delivery correlates with higher revenue (r={corr:.2f})")
                    insights["recommendations"].append("Delivery speed is a competitive advantage. Invest in logistics infrastructure in high-revenue regions.")

    return insights


def generate_regional_insights_text(df, schema):
    """Generate formatted text insights for display."""
    analysis = analyze_regional_performance(df, schema)

    if "error" in analysis:
        return f"⚠️ {analysis['error']}"

    lines = [
        "=" * 60,
        "🌎 REGIONAL INTELLIGENCE REPORT",
        "=" * 60,
        ""
    ]

    if "top_region" in analysis:
        lines.extend([
            f"🏆 Top Region: {analysis['top_region']}",
            f"💰 Top Region Revenue: ${analysis['top_region_revenue']:,.2f}",
            f"📊 Market Share: {analysis['top_region_share']}%",
            f"🌍 Total Regions: {analysis['region_count']}",
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
