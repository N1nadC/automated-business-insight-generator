import pandas as pd

from insights.revenue_insights import analyze_revenue_trends
from insights.product_insights import analyze_product_performance
from insights.customer_insights import analyze_customer_behavior
from insights.regional_insights import analyze_regional_performance
from insights.delivery_insights import analyze_delivery_performance


def generate_comprehensive_insights(df, schema):
    """
    Generate comprehensive AI-powered business insights across all dimensions.
    Returns structured insights with findings, recommendations, risks, and opportunities.
    """

    insights = {
        "executive_summary": "",
        "revenue": {},
        "product": {},
        "customer": {},
        "regional": {},
        "delivery": {},
        "strategic_recommendations": [],
        "critical_risks": [],
        "top_opportunities": []
    }

    # Collect all analyses
    insights["revenue"] = analyze_revenue_trends(df, schema)
    insights["product"] = analyze_product_performance(df, schema)
    insights["customer"] = analyze_customer_behavior(df, schema)
    insights["regional"] = analyze_regional_performance(df, schema)
    insights["delivery"] = analyze_delivery_performance(df, schema)

    # ── Strategic Synthesis ──
    all_recommendations = []
    all_risks = []
    all_opportunities = []

    for dimension in ["revenue", "product", "customer", "regional", "delivery"]:
        data = insights[dimension]
        if "error" not in data:
            all_recommendations.extend(data.get("recommendations", []))
            all_risks.extend(data.get("risks", []))
            all_opportunities.extend(data.get("opportunities", []))

    # Prioritize: risks first, then recommendations, then opportunities
    insights["critical_risks"] = all_risks[:5]  # Top 5 risks
    insights["strategic_recommendations"] = all_recommendations[:7]  # Top 7 actions
    insights["top_opportunities"] = all_opportunities[:5]  # Top 5 opportunities

    # ── Executive Narrative ──
    narrative_lines = [
        "🎯 EXECUTIVE STRATEGIC BRIEFING",
        "=" * 60,
        ""
    ]

    # Revenue headline
    if "total_revenue" in insights["revenue"]:
        rev = insights["revenue"]["total_revenue"]
        growth = insights["revenue"].get("growth_rate", 0)
        narrative_lines.append(f"💰 REVENUE: ${rev:,.2f} | Growth: {growth:+.1f}%")

    # Customer headline
    if "total_customers" in insights["customer"]:
        cust = insights["customer"]["total_customers"]
        repeat = insights["customer"].get("repeat_customer_rate", 0)
        narrative_lines.append(f"👥 CUSTOMERS: {cust:,} | Repeat Rate: {repeat:.1f}%")

    # Delivery headline
    if "avg_days" in insights["delivery"]:
        days = insights["delivery"]["avg_days"]
        sla7 = insights["delivery"].get("sla_7day", 0)
        narrative_lines.append(f"🚚 DELIVERY: {days:.1f} days avg | {sla7:.1f}% within 7 days")

    narrative_lines.append("")

    # Critical alerts
    if insights["critical_risks"]:
        narrative_lines.append("🚨 CRITICAL ALERTS")
        narrative_lines.append("-" * 40)
        for i, risk in enumerate(insights["critical_risks"][:3], 1):
            narrative_lines.append(f"  {i}. {risk}")
        narrative_lines.append("")

    # Strategic priorities
    if insights["strategic_recommendations"]:
        narrative_lines.append("💡 STRATEGIC PRIORITIES")
        narrative_lines.append("-" * 40)
        for i, rec in enumerate(insights["strategic_recommendations"][:5], 1):
            narrative_lines.append(f"  {i}. {rec}")
        narrative_lines.append("")

    # Quick wins
    if insights["top_opportunities"]:
        narrative_lines.append("⭐ QUICK WINS")
        narrative_lines.append("-" * 40)
        for i, opp in enumerate(insights["top_opportunities"][:3], 1):
            narrative_lines.append(f"  {i}. {opp}")
        narrative_lines.append("")

    narrative_lines.append("=" * 60)
    insights["executive_summary"] = "\n".join(narrative_lines)

    return insights


def generate_executive_insights_text(df, schema):
    """Generate the full executive insights text for display."""
    comprehensive = generate_comprehensive_insights(df, schema)
    return comprehensive["executive_summary"]
