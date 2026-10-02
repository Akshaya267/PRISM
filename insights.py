import pandas as pd
from typing import List, Dict, Any, Optional
from app.models.schemas import Insight
from app.analytics.engine import (
    analyze_trends,
    analyze_contributions,
    detect_anomalies,
    analyze_correlations
)
from app.root_cause.reasoning import deduce_root_causes
from app.evidence.tracer import build_evidence_trail

def generate_insights(df: pd.DataFrame, overview: Any) -> List[Insight]:
    """
    Orchestrates statistical engines and generates traceable Insight objects.
    """
    insights: List[Insight] = []

    dims = overview.detected_dimensions
    date_col = dims.get("date")
    rev_col = dims.get("revenue") or dims.get("sales")
    prof_col = dims.get("profit")
    qty_col = dims.get("quantity")

    numeric_cols = [c for c in [rev_col, prof_col, qty_col] if c and c in df.columns]
    dimension_cols = [dims.get(k) for k in ["region", "product", "category", "customer"] if dims.get(k) and dims.get(k) in df.columns]

    # 1. Trend Analysis & Contribution Breakdown
    if date_col and numeric_cols:
        trend_results = analyze_trends(df, date_col, numeric_cols)

        ins_counter = 1
        for metric, stats in trend_results.get("metrics", {}).items():
            prev_val = stats["previous_value"]
            curr_val = stats["current_value"]
            change_pct = stats["change_pct"]
            abs_change = abs(change_pct)

            if abs_change < 1.0:
                continue  # Ignore trivial changes

            # Calculate contributions
            contributions = analyze_contributions(df, date_col, metric, dimension_cols)

            # Deduce root causes
            causes = deduce_root_causes(df, metric, metric, dims, trend_results)

            # Supporting factors compilation
            supporting_factors = []
            if contributions:
                top_c = contributions[0]
                supporting_factors.append(f"{top_c['dimension']} '{top_c['value']}' contributed {top_c['contribution_percent']}% of overall metric shift.")

            if causes:
                cause = causes[0]
                if cause.get("operational_bottleneck"):
                    supporting_factors.append(f"Operational Factor: {cause['operational_bottleneck']}")

            # Affected segment label
            affected_segment = "Overall Business"
            if contributions:
                affected_segment = f"{contributions[0]['dimension']}: {contributions[0]['value']}"
            elif causes:
                affected_segment = causes[0]["primary_affected_segment"]

            # Severity score & Impact category
            if abs_change >= 10.0:
                impact = "HIGH"
                severity_score = min(10.0, 7.0 + (abs_change / 20.0))
            elif abs_change >= 5.0:
                impact = "MEDIUM"
                severity_score = 5.0 + (abs_change / 10.0)
            else:
                impact = "LOW"
                severity_score = 3.0 + (abs_change / 5.0)

            ins_id = f"INS-{ins_counter:03d}"
            ins_counter += 1

            direction_str = "Decline" if change_pct < 0 else "Growth"
            title = f"{metric.title()} {direction_str} Concentrated in {affected_segment}"
            what_happened = f"{metric.title()} shifted by {change_pct:+.1f}% from {prev_val:,.2f} to {curr_val:,.2f} in the current period."

            suggested_action = (
                f"Review operational performance and inventory availability for {affected_segment}."
                if change_pct < 0
                else f"Scale successful sales distribution strategies for {affected_segment}."
            )

            # Build Evidence Trail
            evidence = build_evidence_trail(
                insight_id=ins_id,
                claim=f"{metric.title()} changed by {change_pct:+.1f}%",
                metric_name=metric,
                current_val=curr_val,
                previous_val=prev_val,
                top_contributors=contributions,
                supporting_factors=supporting_factors,
                methods_used=["Period Comparison", "Contribution Waterfall", "Segment Attribution"],
                confidence="HIGH" if len(supporting_factors) >= 2 else "MEDIUM"
            )

            insights.append(Insight(
                id=ins_id,
                title=title,
                impact=impact,
                severity_score=round(severity_score, 1),
                what_happened=what_happened,
                metric_name=metric,
                change_pct=change_pct,
                affected_segment=affected_segment,
                confidence=evidence.confidence,
                suggested_action=suggested_action,
                evidence=evidence
            ))

    # 2. Anomaly Insights
    if numeric_cols:
        anomalies = detect_anomalies(df, numeric_cols, date_col)
        if anomalies:
            top_anomaly = anomalies[0]
            ins_id = f"INS-ANO-{len(insights)+1:02d}"
            title = f"Statistical Anomaly Detected in {top_anomaly['metric'].title()}"
            what_happened = f"Observed value {top_anomaly['value']:,.2f} on {top_anomaly.get('date', 'recent record')} was outside normal bounds ({top_anomaly['expected_range']}) with a Z-score of {top_anomaly['z_score']}."

            evidence = build_evidence_trail(
                insight_id=ins_id,
                claim=f"Unusual spike/drop in {top_anomaly['metric']}",
                metric_name=top_anomaly['metric'],
                current_val=top_anomaly['value'],
                previous_val=df[top_anomaly['metric']].mean(),
                top_contributors=[],
                supporting_factors=[f"Context: {top_anomaly['context']}", f"Z-score: {top_anomaly['z_score']}"],
                methods_used=["IQR Outlier Test", "Z-score Anomaly Detection"],
                confidence="HIGH"
            )

            insights.append(Insight(
                id=ins_id,
                title=title,
                impact=top_anomaly["severity"],
                severity_score=8.5,
                what_happened=what_happened,
                metric_name=top_anomaly['metric'],
                change_pct=round(top_anomaly['z_score'] * 10.0, 1),
                affected_segment=top_anomaly['context'],
                confidence="HIGH",
                suggested_action=f"Investigate root cause of outlier event in {top_anomaly['context']}.",
                evidence=evidence
            ))

    # Sort insights by severity score descending
    insights.sort(key=lambda x: x.severity_score, reverse=True)
    return insights
