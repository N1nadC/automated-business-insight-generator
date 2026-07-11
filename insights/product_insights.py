import pandas as pd
import numpy as np

from analytics.dynamic.product_analysis import (
    get_top_category
)


def product_summary(df=None, schema=None):
    """
    Legacy simple product summary for reports.executive_summary compatibility.
    """
    if df is not None and schema is not None:
        top = get_top_category(df, schema)
        return (
            f"The highest-performing product category "
            f"was '{top['category']}', generating "
            f"${top['revenue']:,.2f} in revenue."
        )
    return "Product data not available."


def analyze_product_performance(df, schema):
    """
    Deep product and category analysis with concentration metrics,
    underperformer identification, and portfolio recommendations.
    """
    revenue_col = schema.get("revenue")
    category_col = schema.get("category")
    product_col = schema.get("product")

    if not revenue_col:
        return {"error": "Revenue column not detected"}

    df = df.copy()
    df[revenue_col] = pd.to_numeric(df[revenue_col], errors="coerce")

    insights = {
        "findings": [],
        "recommendations": [],
        "risks": [],
        "opportunities": []
    }

    # ── Category Analysis ──
    if category_col:
        category_perf = df.groupby(category_col)[revenue_col].sum().sort_values(ascending=False)
        total_revenue = category_perf.sum()

        insights["top_category"] = category_perf.index[0]
        insights["top_category_revenue"] = float(category_perf.iloc[0])
        insights["top_category_share"] = round(category_perf.iloc[0] / total_revenue * 100, 1)
        insights["category_count"] = len(category_perf)

        # Concentration analysis (Herfindahl index)
        shares = (category_perf / total_revenue) ** 2
        hhi = shares.sum() * 10000
        insights["hhi"] = round(hhi, 0)

        if hhi > 2500:
            insights["findings"].append(f"⚠️ HIGH CONCENTRATION: Top category '{insights['top_category']}' dominates with {insights['top_category_share']}% of revenue (HHI: {hhi:.0f}).")
            insights["risks"].append("PORTFOLIO RISK: Over-reliance on one category. Any disruption (supply chain, trend shift) will severely impact revenue.")
            insights["recommendations"].append("URGENT: Diversify category portfolio. Target 3-4 strong categories with no single one >40% share.")
        elif hhi > 1500:
            insights["findings"].append(f"📊 MODERATE CONCENTRATION: '{insights['top_category']}' leads with {insights['top_category_share']}% (HHI: {hhi:.0f}).")
            insights["recommendations"].append("Grow secondary categories. Cross-sell complementary products to reduce dependency.")
        else:
            insights["findings"].append(f"✅ BALANCED PORTFOLIO: '{insights['top_category']}' leads with {insights['top_category_share']}% (HHI: {hhi:.0f}). Well diversified.")
            insights["opportunities"].append("Leverage diversification to test new categories with low risk.")

        # Bottom performers
        bottom_3 = category_perf.tail(3)
        bottom_revenue = bottom_3.sum()
        bottom_share = bottom_revenue / total_revenue * 100

        insights["findings"].append(f"📉 Bottom 3 categories contribute only {bottom_share:.1f}% of revenue: {', '.join(bottom_3.index.tolist())}")

        if bottom_share < 5:
            insights["recommendations"].append(f"Consider discontinuing or rebranding underperformers: {', '.join(bottom_3.index.tolist())}. Resources better allocated to growth categories.")
        else:
            insights["recommendations"].append(f"Investigate why {', '.join(bottom_3.index.tolist())} underperform — pricing, quality, or marketing gaps?")

        # Long tail analysis
        long_tail = category_perf[category_perf < category_perf.mean()]
        long_tail_share = long_tail.sum() / total_revenue * 100
        insights["findings"].append(f"📏 Long tail: {len(long_tail)} categories below average contribute {long_tail_share:.1f}% of revenue.")

        if len(long_tail) > 10:
            insights["recommendations"].append("Simplify SKU portfolio. Too many low-performing categories increase operational complexity without proportional returns.")

    # ── Product Analysis ──
    if product_col:
        product_perf = df.groupby(product_col)[revenue_col].sum().sort_values(ascending=False)

        insights["product_count"] = len(product_perf)
        insights["top_product"] = product_perf.index[0]
        insights["top_product_revenue"] = float(product_perf.iloc[0])

        # Pareto analysis (80/20 rule)
        cumulative = product_perf.cumsum() / product_perf.sum()
        pareto_80 = (cumulative <= 0.80).sum()
        pareto_20_pct = pareto_80 / len(product_perf) * 100

        insights["findings"].append(f"🎯 Pareto Analysis: Top {pareto_80} products ({pareto_20_pct:.1f}%) generate 80% of revenue.")

        if pareto_20_pct < 15:
            insights["opportunities"].append("Highly efficient product mix. Double down on top performers with bundling and premium variants.")
        elif pareto_20_pct > 30:
            insights["risks"].append("INEFFICIENT MIX: Too many products drive 80% of revenue. High inventory complexity. Rationalize slow movers.")
            insights["recommendations"].append("Conduct ABC analysis. Eliminate C-class products or move them to made-to-order.")

        # Zero-revenue products (if any)
        zero_rev = (product_perf == 0).sum()
        if zero_rev > 0:
            insights["risks"].append(f"DEAD STOCK: {zero_rev} products with zero revenue. Immediate inventory write-off recommended.")

    return insights


def generate_product_insights_text(df, schema):
    """Generate formatted text insights for display."""
    analysis = analyze_product_performance(df, schema)

    if "error" in analysis:
        return f"⚠️ {analysis['error']}"

    lines = [
        "=" * 60,
        "🛒 PRODUCT INTELLIGENCE REPORT",
        "=" * 60,
        ""
    ]

    if "top_category" in analysis:
        lines.extend([
            f"🏆 Top Category: {analysis['top_category']}",
            f"💰 Top Category Revenue: ${analysis['top_category_revenue']:,.2f}",
            f"📊 Market Share: {analysis['top_category_share']}%",
            f"📦 Total Categories: {analysis['category_count']}",
            f"📈 Concentration (HHI): {analysis['hhi']}",
        ])

    if "product_count" in analysis:
        lines.extend([
            "",
            f"🎯 Top Product: {analysis['top_product']}",
            f"💰 Top Product Revenue: ${analysis['top_product_revenue']:,.2f}",
            f"📦 Total Products: {analysis['product_count']}",
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
