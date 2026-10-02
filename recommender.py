from typing import List
from app.models.schemas import Insight, Recommendation

def generate_recommendations(insights: List[Insight]) -> List[Recommendation]:
    """
    Generates evidence-grounded action recommendations directly derived from detected insights.
    """
    recommendations: List[Recommendation] = []

    for idx, ins in enumerate(insights, start=1):
        rec_id = f"REC-{idx:03d}"
        ev = ins.evidence
        metric_clean = ins.metric_name.title()
        segment_str = ins.affected_segment

        # Extract top contributor details if available
        top_contrib_text = ""
        if ev.top_contributors:
            top = ev.top_contributors[0]
            top_contrib_text = f" ({top.dimension} {top.value} contributed {top.contribution_percent}% of change)"

        # Check for inventory context in supporting factors
        is_inventory_issue = any("inventory" in f.lower() or "stock" in f.lower() for f in ev.supporting_factors)
        is_revenue_issue = "revenue" in ins.metric_name.lower() or "sales" in ins.metric_name.lower()
        is_anomaly = "anomaly" in ins.title.lower() or "unusual" in ins.title.lower()

        if is_inventory_issue and is_revenue_issue:
            action = f"Optimize inventory allocation and replenishment cycle for {segment_str}."
            why = f"{metric_clean} changed by {ins.change_pct:+.1f}%{top_contrib_text} while inventory availability remained below average thresholds."
            objective = "Mitigate lost revenue and prevent stock-outs in high-demand channels."
            category = "Inventory & Logistics"
            monitor = [f"{metric_clean} Recovery", "Safety Stock Levels", "Stock-out Frequency"]
        elif is_revenue_issue and ins.change_pct < 0:
            action = f"Initiate targeted commercial review for {segment_str}."
            why = f"{metric_clean} declined by {ins.change_pct:.1f}% in the current evaluation period{top_contrib_text}."
            objective = "Stabilize sales volume and identify root-cause customer churn or pricing friction."
            category = "Sales Strategy"
            monitor = [f"{metric_clean} Growth", "Order Conversion Rate", "Customer Retention"]
        elif is_anomaly:
            action = f"Audit data entry and operational events for {segment_str}."
            why = f"A statistical anomaly ({ins.what_happened}) was detected outside normal expectation boundaries."
            objective = "Verify record accuracy and isolate isolated operational disruptions."
            category = "Data & Operations"
            monitor = ["Record Accuracy", "Daily Variance", "System Integrity"]
        else:
            action = f"Capitalize on positive momentum in {segment_str}."
            why = f"{metric_clean} surged by {ins.change_pct:+.1f}%{top_contrib_text}."
            objective = "Expand capacity and scale successful distribution strategies."
            category = "Growth & Expansion"
            monitor = [f"{metric_clean} Retention", "Margin Percentage", "Customer Demand"]

        recommendations.append(Recommendation(
            id=rec_id,
            title=f"Action Plan for {segment_str}",
            action=action,
            why=why,
            supporting_evidence_id=ins.id,
            expected_objective=objective,
            priority=ins.impact,
            confidence=ins.confidence,
            monitor=monitor,
            dimension_category=category
        ))

    return recommendations
