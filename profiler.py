import re
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from schemas import ColumnProfile, DataOverview

def infer_semantic_role(col_name: str, series: pd.Series) -> str:
    name_clean = col_name.lower().replace("_", "").replace(" ", "").replace("-", "")
    
    # Check temporal first
    if any(k in name_clean for k in ["date", "time", "timestamp", "year", "month", "day", "period"]):
        return "temporal"
    
    # Try parsing date if series looks like date strings
    if series.dtype == "object":
        sample = series.dropna().head(10).astype(str)
        # Check if sample strings look like dates (YYYY-MM-DD or MM/DD/YYYY)
        date_pattern_matches = sum(bool(re.search(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{4}", s)) for s in sample)
        if len(sample) > 0 and date_pattern_matches / len(sample) > 0.5:
            return "temporal"

    # Monetary metrics
    monetary_keywords = ["revenue", "sales", "cost", "profit", "price", "amount", "margin", "income", "spend", "earning", "turnover", "fee", "val", "value"]
    if any(k in name_clean for k in monetary_keywords):
        return "monetary"
        
    # Volume metrics
    volume_keywords = ["qty", "quantity", "units", "inventory", "stock", "volume", "count", "orders", "num", "number"]
    if any(k in name_clean for k in volume_keywords):
        return "volume"

    # Geographic dimension
    geo_keywords = ["region", "country", "city", "state", "territory", "zone", "location", "area", "market"]
    if any(k in name_clean for k in geo_keywords):
        return "geographic"

    # Product dimension
    prod_keywords = ["product", "item", "sku", "category", "brand", "model", "service"]
    if any(k in name_clean for k in prod_keywords):
        return "product"

    # Customer dimension
    cust_keywords = ["customer", "client", "user", "buyer", "segment", "cohort", "account"]
    if any(k in name_clean for k in cust_keywords):
        return "customer"

    # Identifier
    id_keywords = ["id", "code", "index", "key", "number", "no"]
    if any(k in name_clean for k in id_keywords) and (series.nunique() / max(len(series), 1) > 0.6):
        return "identifier"

    # Numeric fallback vs string fallback
    if pd.api.types.is_numeric_dtype(series):
        return "generic_numeric"
    else:
        return "generic_string"


def profile_dataset(df: pd.DataFrame, dataset_name: str = "Uploaded Dataset", extra_warnings: List[str] = None) -> DataOverview:
    total_rows = len(df)
    total_cols = len(df.columns)
    warnings = list(extra_warnings or [])

    col_profiles: List[ColumnProfile] = []
    detected_dimensions: Dict[str, Optional[str]] = {
        "date": None,
        "revenue": None,
        "sales": None,
        "cost": None,
        "profit": None,
        "quantity": None,
        "inventory": None,
        "region": None,
        "product": None,
        "customer": None,
        "category": None
    }

    key_metrics: Dict[str, float] = {}

    date_range: Optional[Dict[str, str]] = None
    total_missing_cells = 0

    for col in df.columns:
        series = df[col]
        missing_count = int(series.isna().sum())
        total_missing_cells += missing_count
        missing_pct = round((missing_count / max(total_rows, 1)) * 100, 2)
        unique_count = int(series.nunique(dropna=True))

        role = infer_semantic_role(col, series)

        # Map to specific detected dimension slots if not filled
        col_clean = col.lower()
        if role == "temporal" and not detected_dimensions["date"]:
            detected_dimensions["date"] = col
        elif role == "monetary":
            if "revenue" in col_clean and not detected_dimensions["revenue"]:
                detected_dimensions["revenue"] = col
            elif "profit" in col_clean and not detected_dimensions["profit"]:
                detected_dimensions["profit"] = col
            elif ("cost" in col_clean or "expense" in col_clean) and not detected_dimensions["cost"]:
                detected_dimensions["cost"] = col
            elif ("sales" in col_clean or "amount" in col_clean) and not detected_dimensions["sales"]:
                detected_dimensions["sales"] = col
            elif not detected_dimensions["revenue"]:
                detected_dimensions["revenue"] = col
        elif role == "volume":
            if ("inventory" in col_clean or "stock" in col_clean) and not detected_dimensions["inventory"]:
                detected_dimensions["inventory"] = col
            elif not detected_dimensions["quantity"]:
                detected_dimensions["quantity"] = col
        elif role == "geographic" and not detected_dimensions["region"]:
            detected_dimensions["region"] = col
        elif role == "product":
            if "category" in col_clean and not detected_dimensions["category"]:
                detected_dimensions["category"] = col
            elif not detected_dimensions["product"]:
                detected_dimensions["product"] = col
        elif role == "customer" and not detected_dimensions["customer"]:
            detected_dimensions["customer"] = col

        # Sample values
        sample_vals = series.dropna().head(3).tolist()
        # Ensure sample values are JSON serializable
        clean_sample = []
        for v in sample_vals:
            if isinstance(v, (np.integer, int)):
                clean_sample.append(int(v))
            elif isinstance(v, (np.floating, float)):
                clean_sample.append(round(float(v), 2))
            else:
                clean_sample.append(str(v))

        dtype_str = str(series.dtype)
        col_profiles.append(ColumnProfile(
            name=col,
            semantic_role=role,
            data_type=dtype_str,
            missing_count=missing_count,
            missing_pct=missing_pct,
            unique_count=unique_count,
            sample_values=clean_sample
        ))

        # Warning for high missingness
        if missing_pct > 15.0:
            warnings.append(f"Column '{col}' has {missing_pct}% missing values.")

    # Calculate Date Range if date column identified
    date_col = detected_dimensions["date"]
    if date_col:
        try:
            parsed_dates = pd.to_datetime(df[date_col], errors="coerce")
            valid_dates = parsed_dates.dropna()
            if not valid_dates.empty:
                date_range = {
                    "start": valid_dates.min().strftime("%Y-%m-%d"),
                    "end": valid_dates.max().strftime("%Y-%m-%d")
                }
                invalid_dates = len(parsed_dates) - len(valid_dates)
                if invalid_dates > 0:
                    warnings.append(f"Column '{date_col}' contains {invalid_dates} unparseable date records.")
        except Exception:
            pass

    # Aggregate Key Metrics if columns detected
    for metric_key, mapped_col in [("Revenue", detected_dimensions.get("revenue")), 
                                   ("Sales", detected_dimensions.get("sales")),
                                   ("Profit", detected_dimensions.get("profit")),
                                   ("Cost", detected_dimensions.get("cost")),
                                   ("Quantity", detected_dimensions.get("quantity")),
                                   ("Inventory", detected_dimensions.get("inventory"))]:
        if mapped_col and pd.api.types.is_numeric_dtype(df[mapped_col]):
            key_metrics[f"Total {metric_key}"] = round(float(df[mapped_col].sum()), 2)
            key_metrics[f"Avg {metric_key}"] = round(float(df[mapped_col].mean()), 2)

    # Add Profit Margin if Revenue and Profit exist
    rev_col = detected_dimensions.get("revenue") or detected_dimensions.get("sales")
    prof_col = detected_dimensions.get("profit")
    if rev_col and prof_col and rev_col in df and prof_col in df:
        tot_rev = df[rev_col].sum()
        tot_prof = df[prof_col].sum()
        if tot_rev > 0:
            key_metrics["Profit Margin %"] = round(float((tot_prof / tot_rev) * 100), 2)

    # Data Quality Score
    total_cells = max(total_rows * total_cols, 1)
    missing_pct_overall = round((total_missing_cells / total_cells) * 100, 2)
    duplicate_count = int(df.duplicated().sum())

    score = 100
    score -= min(30, int(missing_pct_overall * 1.5))
    score -= min(20, int((duplicate_count / max(total_rows, 1)) * 100))
    if not date_col:
        score -= 10
    if not rev_col:
        score -= 10
    score = max(30, min(100, score))

    return DataOverview(
        dataset_name=dataset_name,
        total_rows=total_rows,
        total_cols=total_cols,
        date_range=date_range,
        missing_records_pct=missing_pct_overall,
        duplicate_rows=duplicate_count,
        column_profiles=col_profiles,
        detected_dimensions=detected_dimensions,
        key_metrics=key_metrics,
        quality_score=score,
        quality_warnings=warnings
    )
