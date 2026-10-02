import pytest
import pandas as pd
from ingest import load_dataset
from profiler import profile_dataset, infer_semantic_role
from engine import analyze_trends, analyze_contributions, detect_anomalies
from tracer import build_evidence_trail
from recommender import generate_recommendations
from demo_data import generate_demo_dataset

def test_demo_dataset_generation():
    df = generate_demo_dataset()
    assert not df.empty
    assert len(df) > 100
    assert "Revenue" in df.columns
    assert "Region" in df.columns

def test_data_profiling():
    df = generate_demo_dataset()
    overview = profile_dataset(df, "Test Dataset")
    assert overview.total_rows == len(df)
    assert overview.quality_score >= 50
    assert overview.detected_dimensions["revenue"] == "Revenue"
    assert overview.detected_dimensions["region"] == "Region"

def test_trend_analysis():
    df = generate_demo_dataset()
    trends = analyze_trends(df, "Order_Date", ["Revenue", "Profit"])
    assert "metrics" in trends
    assert "Revenue" in trends["metrics"]
    metrics_rev = trends["metrics"]["Revenue"]
    assert "change_pct" in metrics_rev

def test_contribution_analysis():
    df = generate_demo_dataset()
    contribs = analyze_contributions(df, "Order_Date", "Revenue", ["Region", "Product"])
    assert len(contribs) > 0
    assert "contribution_percent" in contribs[0]

def test_anomaly_detection():
    df = generate_demo_dataset()
    anomalies = detect_anomalies(df, ["Revenue"])
    assert isinstance(anomalies, list)

def test_evidence_tracer():
    evidence = build_evidence_trail(
        insight_id="INS-001",
        claim="Revenue decreased 15%",
        metric_name="Revenue",
        current_val=850000.0,
        previous_val=1000000.0,
        top_contributors=[{"dimension": "Region", "value": "South", "contribution_percent": 61.0, "change_value": -91500.0}],
        supporting_factors=["Product A sales declined"]
    )
    assert evidence.insight_id == "INS-001"
    assert evidence.calculation.change_percent == -15.0
    assert len(evidence.top_contributors) == 1
    assert evidence.top_contributors[0].dimension == "Region"
