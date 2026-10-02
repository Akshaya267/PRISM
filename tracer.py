from app.models.schemas import EvidenceDetail, CalculationDetail, ContributionSegment
from typing import List, Dict, Any

def build_evidence_trail(
    insight_id: str,
    claim: str,
    metric_name: str,
    current_val: float,
    previous_val: float,
    top_contributors: List[Dict[str, Any]],
    supporting_factors: List[str],
    methods_used: List[str] = None,
    confidence: str = "HIGH"
) -> EvidenceDetail:
    """
    Constructs an explicit evidence trail object tying numerical facts to an insight.
    """
    change_val = current_val - previous_val
    change_pct = ((change_val / previous_val) * 100) if previous_val != 0 else 0.0

    formula_str = f"({current_val:,.2f} - {previous_val:,.2f}) / {previous_val:,.2f} = {change_pct:+.1f}%"

    calc = CalculationDetail(
        metric=metric_name,
        current_value=round(current_val, 2),
        previous_value=round(previous_val, 2),
        change_value=round(change_val, 2),
        change_percent=round(change_pct, 2),
        formula=formula_str
    )

    contrib_segments = []
    for c in top_contributors:
        contrib_segments.append(ContributionSegment(
            dimension=c.get("dimension", "Segment"),
            value=str(c.get("value", "Unknown")),
            contribution_percent=round(float(c.get("contribution_percent", 0.0)), 2),
            change_value=round(float(c.get("change_value", 0.0)), 2)
        ))

    default_methods = methods_used or ["Period Comparison", "Contribution Analysis", "Statistical Profiling"]

    reasoning_summary = (
        f"Grounded Evidence Trail: Based on deterministic statistical calculation, {metric_name} changed by {change_pct:+.1f}% "
        f"from previous period ({previous_val:,.2f}) to current period ({current_val:,.2f}). "
    )
    if contrib_segments:
        top = contrib_segments[0]
        reasoning_summary += f"The highest contributor was {top.dimension} '{top.value}', accounting for {top.contribution_percent}% of the total variance."

    return EvidenceDetail(
        insight_id=insight_id,
        claim=claim,
        metric_name=metric_name,
        calculation=calc,
        top_contributors=contrib_segments,
        supporting_factors=supporting_factors,
        methods_used=default_methods,
        confidence=confidence,
        analytical_reasoning=reasoning_summary
    )
