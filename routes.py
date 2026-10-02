import pandas as pd
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException
from schemas import DataOverview, Insight, Recommendation, QueryRequest, QueryResponse, EvidenceDetail
from ingest import load_dataset
from profiler import profile_dataset
from insights import generate_insights
from recommender import generate_recommendations
from ask_prism import answer_query
from demo_data import generate_demo_dataset

router = APIRouter(prefix="/api")

# Session state in-memory storage (handles active dataset session)
state: Dict[str, Any] = {
    "df": None,
    "overview": None,
    "insights": [],
    "recommendations": []
}

def _process_dataframe(df: pd.DataFrame, dataset_name: str, extra_warnings: List[str] = None):
    overview = profile_dataset(df, dataset_name=dataset_name, extra_warnings=extra_warnings or [])
    insights = generate_insights(df, overview)
    recommendations = generate_recommendations(insights)

    state["df"] = df
    state["overview"] = overview
    state["insights"] = insights
    state["recommendations"] = recommendations

    return {
        "overview": overview,
        "insights_count": len(insights),
        "recommendations_count": len(recommendations)
    }


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        df, metadata = load_dataset(content, file.filename)
        summary = _process_dataframe(df, dataset_name=file.filename, extra_warnings=metadata.get("warnings", []))
        return {
            "status": "success",
            "filename": file.filename,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/demo")
def load_demo():
    df = generate_demo_dataset()
    summary = _process_dataframe(df, dataset_name="PRISM Business Demo Dataset")
    return {
        "status": "success",
        "dataset_name": "PRISM Business Demo Dataset",
        "summary": summary
    }


@router.get("/overview", response_model=DataOverview)
def get_overview():
    if state["overview"] is None:
        # Auto-load demo if no dataset uploaded yet
        load_demo()
    return state["overview"]


@router.get("/insights", response_model=List[Insight])
def get_insights():
    if state["overview"] is None:
        load_demo()
    return state["insights"]


@router.get("/recommendations", response_model=List[Recommendation])
def get_recommendations():
    if state["overview"] is None:
        load_demo()
    return state["recommendations"]


@router.get("/evidence/{insight_id}", response_model=EvidenceDetail)
def get_evidence(insight_id: str):
    if state["overview"] is None:
        load_demo()
    for ins in state["insights"]:
        if ins.id == insight_id:
            return ins.evidence
    raise HTTPException(status_code=404, detail=f"Evidence for insight '{insight_id}' not found.")


@router.post("/query", response_model=QueryResponse)
def query_prism(request: QueryRequest):
    if state["df"] is None:
        load_demo()
    return answer_query(
        question=request.question,
        df=state["df"],
        overview=state["overview"],
        insights=state["insights"]
    )


@router.get("/charts")
def get_charts():
    if state["df"] is None:
        load_demo()

    df: pd.DataFrame = state["df"]
    overview: DataOverview = state["overview"]
    dims = overview.detected_dimensions

    date_col = dims.get("date")
    rev_col = dims.get("revenue") or dims.get("sales")
    prof_col = dims.get("profit")
    region_col = dims.get("region")
    prod_col = dims.get("product")

    charts_data = {}

    # 1. Trend Over Time Chart
    if date_col and date_col in df.columns and rev_col and rev_col in df.columns:
        df_copy = df.copy()
        df_copy["_parsed_date"] = pd.to_datetime(df_copy[date_col], errors="coerce")
        df_valid = df_copy.dropna(subset=["_parsed_date"]).sort_values("_parsed_date")

        # Group by month or date depending on range
        df_valid["_period"] = df_valid["_parsed_date"].dt.strftime("%Y-%m")
        grouped = df_valid.groupby("_period", observed=False).agg({
            rev_col: "sum",
            prof_col: "sum" if prof_col and prof_col in df.columns else rev_col
        }).reset_index()

        charts_data["trend"] = [
            {
                "period": str(row["_period"]),
                "revenue": round(float(row[rev_col]), 2),
                "profit": round(float(row[prof_col]), 2) if prof_col and prof_col in df.columns else 0.0
            }
            for _, row in grouped.iterrows()
        ]

    # 2. Regional Breakdown Chart
    if region_col and region_col in df.columns and rev_col and rev_col in df.columns:
        reg_grp = df.groupby(region_col, observed=False)[rev_col].sum().reset_index()
        charts_data["region"] = [
            {
                "region": str(row[region_col]),
                "revenue": round(float(row[rev_col]), 2)
            }
            for _, row in reg_grp.iterrows()
        ]

    # 3. Product Performance Chart
    if prod_col and prod_col in df.columns and rev_col and rev_col in df.columns:
        prod_grp = df.groupby(prod_col, observed=False)[rev_col].sum().reset_index().sort_values(rev_col, ascending=False).head(5)
        charts_data["product"] = [
            {
                "product": str(row[prod_col]),
                "revenue": round(float(row[rev_col]), 2)
            }
            for _, row in prod_grp.iterrows()
        ]

    return charts_data


@router.get("/health")
def healthcheck():
    return {
        "status": "online",
        "app": "PRISM - Pattern Reasoning and Insight System for Management",
        "session_active": state["df"] is not None
    }
