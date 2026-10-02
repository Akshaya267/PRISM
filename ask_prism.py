import pandas as pd
from typing import List, Dict, Any, Optional
from app.models.schemas import QueryResponse, Insight

def answer_query(
    question: str,
    df: pd.DataFrame,
    overview: Any,
    insights: List[Insight]
) -> QueryResponse:
    """
    Data-grounded Natural Language Query engine for Ask PRISM.
    Answers strictly using computed metrics and insights, returning an anti-hallucination warning if out of domain.
    """
    q_lower = question.lower().strip()
    dims = overview.detected_dimensions
    rev_col = dims.get("revenue") or dims.get("sales")
    prof_col = dims.get("profit")
    region_col = dims.get("region")
    prod_col = dims.get("product")
    date_col = dims.get("date")

    grounded_facts = []

    # Intent 1: Why did revenue / sales decline?
    if "why" in q_lower or "decline" in q_lower or "drop" in q_lower or "fall" in q_lower:
        rev_insights = [i for i in insights if "revenue" in i.metric_name.lower() or "sales" in i.metric_name.lower()]
        if rev_insights:
            top_ins = rev_insights[0]
            ev = top_ins.evidence
            
            grounded_facts.append(f"Calculation Fact: {ev.claim} (from {ev.calculation.previous_value:,.2f} to {ev.calculation.current_value:,.2f}).")
            
            if ev.top_contributors:
                top = ev.top_contributors[0]
                grounded_facts.append(f"Contribution Fact: {top.dimension} '{top.value}' contributed {top.contribution_percent}% of the total decline.")

            for factor in ev.supporting_factors:
                grounded_facts.append(f"Supporting Evidence: {factor}")

            answer = (
                f"Based on the dataset, {ev.claim}. The decline is primarily concentrated in {top_ins.affected_segment}. "
                f"Data shows: " + " ".join(grounded_facts)
            )

            return QueryResponse(
                question=question,
                answer=answer,
                grounded_facts=grounded_facts,
                supporting_evidence_id=top_ins.id,
                confidence="HIGH",
                data_found=True
            )

    # Intent 2: Which region / segment performed worst or best?
    if ("region" in q_lower or "segment" in q_lower or "worst" in q_lower or "best" in q_lower or "top" in q_lower) and region_col and region_col in df.columns:
        if rev_col and rev_col in df.columns:
            grp = df.groupby(region_col, observed=False)[rev_col].sum().sort_values(ascending=True)
            worst_reg = grp.index[0]
            worst_val = grp.iloc[0]
            best_reg = grp.index[-1]
            best_val = grp.iloc[-1]

            fact1 = f"Lowest performing region by {rev_col}: {worst_reg} with total sum of {worst_val:,.2f}."
            fact2 = f"Highest performing region by {rev_col}: {best_reg} with total sum of {best_val:,.2f}."
            grounded_facts.extend([fact1, fact2])

            answer = f"According to computed metrics, {worst_reg} recorded the lowest total {rev_col} at {worst_val:,.2f}, while {best_reg} recorded the highest at {best_val:,.2f}."
            return QueryResponse(
                question=question,
                answer=answer,
                grounded_facts=grounded_facts,
                supporting_evidence_id=insights[0].id if insights else None,
                confidence="HIGH",
                data_found=True
            )

    # Intent 3: Which product contributed most?
    if ("product" in q_lower or "item" in q_lower) and prod_col and prod_col in df.columns:
        if rev_col and rev_col in df.columns:
            grp = df.groupby(prod_col, observed=False)[rev_col].sum().sort_values(ascending=False)
            top_prod = grp.index[0]
            top_val = grp.iloc[0]
            fact = f"Top product by {rev_col}: {top_prod} generating {top_val:,.2f}."
            grounded_facts.append(fact)

            answer = f"The dataset shows {top_prod} is the highest contributor with total {rev_col} of {top_val:,.2f}."
            return QueryResponse(
                question=question,
                answer=answer,
                grounded_facts=grounded_facts,
                supporting_evidence_id=insights[0].id if insights else None,
                confidence="HIGH",
                data_found=True
            )

    # Intent 4: Anomalies / Unusual changes
    if "unusual" in q_lower or "anomaly" in q_lower or "outlier" in q_lower or "investigate" in q_lower:
        anom_insights = [i for i in insights if "anomaly" in i.title.lower() or "unusual" in i.title.lower()]
        if anom_insights:
            anom = anom_insights[0]
            fact = f"Anomaly Fact: {anom.what_happened}"
            grounded_facts.append(fact)
            answer = f"The analytical engine flagged a statistical anomaly: {anom.what_happened}. Suggested action: {anom.suggested_action}"
            return QueryResponse(
                question=question,
                answer=answer,
                grounded_facts=grounded_facts,
                supporting_evidence_id=anom.id,
                confidence="HIGH",
                data_found=True
            )

    # Intent 5: General summary / what to investigate
    if "summary" in q_lower or "overview" in q_lower or "investigate" in q_lower or "action" in q_lower:
        if insights:
            top_ins = insights[0]
            grounded_facts.append(f"Top Priority Insight: {top_ins.title} ({top_ins.impact} Impact).")
            grounded_facts.append(f"Recommendation: {top_ins.suggested_action}")
            answer = f"The primary priority to investigate is {top_ins.title}. {top_ins.what_happened} Action recommended: {top_ins.suggested_action}"
            return QueryResponse(
                question=question,
                answer=answer,
                grounded_facts=grounded_facts,
                supporting_evidence_id=top_ins.id,
                confidence="HIGH",
                data_found=True
            )

    # Fallback Anti-hallucination response
    return QueryResponse(
        question=question,
        answer="I don't have enough evidence in the current dataset to answer that question reliably.",
        grounded_facts=[],
        supporting_evidence_id=None,
        confidence="LOW",
        data_found=False
    )
