from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ColumnProfile(BaseModel):
    name: str
    semantic_role: str  # monetary, volume, temporal, geographic, identifier, product, customer, category, generic_numeric, generic_string
    data_type: str
    missing_count: int
    missing_pct: float
    unique_count: int
    sample_values: List[Any] = Field(default_factory=list)

class DataOverview(BaseModel):
    dataset_name: str
    total_rows: int
    total_cols: int
    date_range: Optional[Dict[str, str]] = None
    missing_records_pct: float
    duplicate_rows: int
    column_profiles: List[ColumnProfile]
    detected_dimensions: Dict[str, Optional[str]]  # role -> col_name mapping
    key_metrics: Dict[str, float]
    quality_score: int  # 0 to 100
    quality_warnings: List[str]

class CalculationDetail(BaseModel):
    metric: str
    current_value: float
    previous_value: float
    change_value: float
    change_percent: float
    formula: str

class ContributionSegment(BaseModel):
    dimension: str
    value: str
    contribution_percent: float
    change_value: float

class EvidenceDetail(BaseModel):
    insight_id: str
    claim: str
    metric_name: str
    calculation: CalculationDetail
    top_contributors: List[ContributionSegment]
    supporting_factors: List[str]
    methods_used: List[str]
    confidence: str  # HIGH, MEDIUM, LOW
    analytical_reasoning: str

class Insight(BaseModel):
    id: str
    title: str
    impact: str  # HIGH, MEDIUM, LOW
    severity_score: float
    what_happened: str
    metric_name: str
    change_pct: float
    affected_segment: str
    confidence: str
    suggested_action: str
    evidence: EvidenceDetail

class Recommendation(BaseModel):
    id: str
    title: str
    action: str
    why: str
    supporting_evidence_id: str
    expected_objective: str
    priority: str  # HIGH, MEDIUM, LOW
    confidence: str
    monitor: List[str]
    dimension_category: str

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    grounded_facts: List[str]
    supporting_evidence_id: Optional[str] = None
    confidence: str
    data_found: bool
