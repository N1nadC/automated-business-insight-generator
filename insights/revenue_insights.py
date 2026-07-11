import pandas as pd
import numpy as np

from analytics.dynamic.revenue_analysis import (
    get_total_revenue,
    get_average_order_value
)


def revenue_summary(df=None, schema=None):
    """
    Legacy simple revenue summary for reports.executive_summary compatibility.
    """
    if df is not None and schema is not None:
        revenue = get_total_revenue(df, schema)
        aov = get_average_order_value(df, schema)
        return (
            f"Total revenue generated was "
            f"${revenue:,.2f}. "
            f"The average order value was "
            f"${aov:,.2f}, indicating the average customer spending per transaction."
        )
    return "Revenue data not available."


def analyze_revenue_trends(df, schema):
    """
    Deep revenue trend analysis with growth rates, seasonality, and anomalies.
    """
    revenue_col = schema.get("revenue")
    date_col = schema.get("date")

    if not revenue_col or not date_col:
        return {"error": "Revenue or date column not detected"}

    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df[revenue_col] = pd.to_numeric(df[revenue_col], errors="coerce")

    # Monthly aggregation
    df["month"] = df[date_col].dt.to_period("M")
    monthly = df.groupby("month")[revenue_col].sum().reset_index()
    monthly["month"] = monthly["month"].astype(str)
    monthly = monthly.sort_values("month")

    n_months = len(monthly)

    insights = {
        "total_revenue": float(monthly[revenue_col].sum()),
        "avg_monthly_revenue": float(monthly[revenue_col].mean()),
        "months_analyzed": n_months,
        "findings": [],
        "recommendations": [],
        "risks": [],
        "opportunities": []
    }

    if n_months >= 2:
        # Growth trend
        first_half = monthly.iloc[:n_months//2][revenue_col].mean()
        second_half = monthly.iloc[n_months//2:][revenue_col].mean()
        growth_rate = ((second_half - first_half) / first_half * 100) if first_half > 0 else 0
        insights["growth_rate"] = round(growth_rate, 1)

        if growth_rate > 20:
            insights["findings"].append(f"🚀 Strong growth trajectory: +{growth_rate:.1f}% revenue increase in recent months.")
            insights["opportunities"].append("Scale operations — demand is outpacing supply. Consider inventory expansion.")
        elif growth_rate > 5:
            insights["findings"].append(f"📈 Steady growth: +{growth_rate:.1f}% revenue increase.")
        elif growth_rate > -5:
            insights["findings"].append(f"➡️ Revenue plateau: {growth_rate:.1f}% change — growth has stalled.")
            insights["recommendations"].append("Launch promotional campaigns or explore new customer segments to reactivate growth.")
        else:
            insights["findings"].append(f"📉 Declining revenue: {growth_rate:.1f}% decrease — immediate attention required.")
            insights["risks"].append("REVENUE DECLINE: Investigate root causes — pricing, competition, or product-market fit.")
            insights["recommendations"].append("Urgent: Conduct customer exit interviews and competitive pricing analysis.")

    if n_months >= 3:
        # Volatility / consistency
        std_dev = monthly[revenue_col].std()
        mean_rev = monthly[revenue_col].mean()
        cv = (std_dev / mean_rev * 100) if mean_rev > 0 else 0
        insights["volatility"] = round(cv, 1)

        if cv > 50:
            insights["findings"].append(f"⚠️ High revenue volatility (CV: {cv:.1f}%) — inconsistent monthly performance.")
            insights["risks"].append("VOLATILITY: Unpredictable cash flow makes planning difficult. Diversify revenue streams.")
        elif cv > 25:
            insights["findings"].append(f"📊 Moderate volatility (CV: {cv:.1f}%) — some seasonality detected.")
            insights["recommendations"].append("Build cash reserves for low months. Consider subscription models for stability.")
        else:
            insights["findings"].append(f"✅ Stable revenue (CV: {cv:.1f}%) — predictable and reliable.")

    if n_months >= 6:
        # Best and worst months
        best_month = monthly.loc[monthly[revenue_col].idxmax()]
        worst_month = monthly.loc[monthly[revenue_col].idxmin()]
        insights["best_month"] = str(best_month["month"])
        insights["best_month_revenue"] = float(best_month[revenue_col])
        insights["worst_month"] = str(worst_month["month"])
        insights["worst_month_revenue"] = float(worst_month[revenue_col])

        insights["findings"].append(f"🏆 Peak month: {best_month['month']} (${best_month[revenue_col]:,.2f})")
        insights["findings"].append(f"📉 Trough month: {worst_month['month']} (${worst_month[revenue_col]:,.2f})")

        # Seasonality pattern
        monthly["month_num"] = pd.to_datetime(monthly["month"]).dt.month
        seasonal = monthly.groupby("month_num")[revenue_col].mean()
        peak_season = seasonal.idxmax()
        low_season = seasonal.idxmin()

        season_names = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                       7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
        insights["findings"].append(f"🗓️ Seasonal peak: {season_names[peak_season]} | Seasonal low: {season_names[low_season]}")
        insights["recommendations"].append(f"Plan marketing spend heavily in Q{((peak_season-1)//3)+1} to capitalize on seasonal demand.")

    # Anomaly detection (simple Z-score)
    if n_months >= 4:
        monthly["zscore"] = (monthly[revenue_col] - monthly[revenue_col].mean()) / monthly[revenue_col].std()
        anomalies = monthly[abs(monthly["zscore"]) > 2]
        if len(anomalies) > 0:
            for _, row in anomalies.iterrows():
                direction = "spike" if row["zscore"] > 0 else "drop"
                insights["findings"].append(f"🚨 Anomaly: {row['month']} shows unusual revenue {direction} (${row[revenue_col]:,.2f})")
            insights["recommendations"].append("Investigate anomalous months — identify one-time events vs. systemic issues.")

    return insights


def generate_revenue_insights_text(df, schema):
    """Generate formatted text insights for display."""
    analysis = analyze_revenue_trends(df, schema)

    if "error" in analysis:
        return f"⚠️ {analysis['error']}"

    lines = [
        "=" * 60,
        "💰 REVENUE INTELLIGENCE REPORT",
        "=" * 60,
        "",
        f"📊 Total Revenue: ${analysis['total_revenue']:,.2f}",
        f"📅 Period: {analysis['months_analyzed']} months",
        f"📈 Avg Monthly: ${analysis['avg_monthly_revenue']:,.2f}",
    ]

    if "growth_rate" in analysis:
        lines.append(f"🚀 Growth Rate: {analysis['growth_rate']:+.1f}%")
    if "volatility" in analysis:
        lines.append(f"📊 Volatility (CV): {analysis['volatility']:.1f}%")

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
