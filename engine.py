import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple

def analyze_trends(df: pd.DataFrame, date_col: str, metric_cols: List[str]) -> Dict[str, Any]:
    """
    Splits data chronologically into previous vs current period and calculates period-over-period change.
    """
    results = {}
    if not date_col or date_col not in df.columns:
        return results

    df_copy = df.copy()
    df_copy["_parsed_date"] = pd.to_datetime(df_copy[date_col], errors="coerce")
    df_clean = df_copy.dropna(subset=["_parsed_date"]).sort_values("_parsed_date")

    if len(df_clean) < 4:
        return results

    mid_idx = len(df_clean) // 2
    prev_df = df_clean.iloc[:mid_idx]
    curr_df = df_clean.iloc[mid_idx:]

    prev_start = prev_df["_parsed_date"].min().strftime("%Y-%m-%d")
    prev_end = prev_df["_parsed_date"].max().strftime("%Y-%m-%d")
    curr_start = curr_df["_parsed_date"].min().strftime("%Y-%m-%d")
    curr_end = curr_df["_parsed_date"].max().strftime("%Y-%m-%d")

    results["periods"] = {
        "previous": f"{prev_start} to {prev_end}",
        "current": f"{curr_start} to {curr_end}"
    }

    results["metrics"] = {}

    for metric in metric_cols:
        if metric in df_clean and pd.api.types.is_numeric_dtype(df_clean[metric]):
            prev_val = float(prev_df[metric].sum())
            curr_val = float(curr_df[metric].sum())
            change_val = curr_val - prev_val
            change_pct = ((change_val / prev_val) * 100) if prev_val != 0 else 0.0

            results["metrics"][metric] = {
                "previous_value": round(prev_val, 2),
                "current_value": round(curr_val, 2),
                "change_value": round(change_val, 2),
                "change_pct": round(change_pct, 2),
                "direction": "increased" if change_val > 0 else ("decreased" if change_val < 0 else "stable")
            }

    return results


def analyze_contributions(df: pd.DataFrame, date_col: Optional[str], metric_col: str, dimension_cols: List[str]) -> List[Dict[str, Any]]:
    """
    Identifies which dimension values contributed most to the change in metric_col.
    """
    contributions = []
    if metric_col not in df.columns or not pd.api.types.is_numeric_dtype(df[metric_col]):
        return contributions

    df_copy = df.copy()
    if date_col and date_col in df.columns:
        df_copy["_parsed_date"] = pd.to_datetime(df_copy[date_col], errors="coerce")
        df_clean = df_copy.dropna(subset=["_parsed_date"]).sort_values("_parsed_date")
        if len(df_clean) >= 4:
            mid_idx = len(df_clean) // 2
            prev_df = df_clean.iloc[:mid_idx]
            curr_df = df_clean.iloc[mid_idx:]
        else:
            prev_df = df_clean.iloc[:len(df_clean)//2]
            curr_df = df_clean.iloc[len(df_clean)//2:]
    else:
        # Split by index half
        mid_idx = len(df) // 2
        prev_df = df.iloc[:mid_idx]
        curr_df = df.iloc[mid_idx:]

    total_prev = prev_df[metric_col].sum()
    total_curr = curr_df[metric_col].sum()
    total_delta = total_curr - total_prev

    if total_delta == 0:
        return contributions

    for dim in dimension_cols:
        if dim not in df.columns:
            continue

        prev_grp = prev_df.groupby(dim, observed=False)[metric_col].sum()
        curr_grp = curr_df.groupby(dim, observed=False)[metric_col].sum()

        all_keys = set(prev_grp.index).union(set(curr_grp.index))
        dim_changes = []

        for key in all_keys:
            val_prev = float(prev_grp.get(key, 0))
            val_curr = float(curr_grp.get(key, 0))
            val_delta = val_curr - val_prev
            
            # Contribution percentage relative to overall change
            contrib_pct = (val_delta / total_delta * 100) if total_delta != 0 else 0

            dim_changes.append({
                "dimension": dim,
                "value": str(key),
                "previous_value": round(val_prev, 2),
                "current_value": round(val_curr, 2),
                "change_value": round(val_delta, 2),
                "contribution_percent": round(contrib_pct, 2)
            })

        # Sort by largest magnitude of contribution
        dim_changes.sort(key=lambda x: abs(x["contribution_percent"]), reverse=True)
        contributions.extend(dim_changes[:3])  # top 3 per dimension

    return contributions


def detect_anomalies(df: pd.DataFrame, metric_cols: List[str], date_col: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Detects statistical anomalies using IQR and Z-score methods.
    """
    anomalies = []

    for metric in metric_cols:
        if metric not in df.columns or not pd.api.types.is_numeric_dtype(df[metric]):
            continue

        series = df[metric].dropna()
        if len(series) < 5:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        mean_val = series.mean()
        std_val = series.std()

        for idx, val in series.items():
            is_iqr_outlier = val < lower_bound or val > upper_bound
            z_score = (val - mean_val) / std_val if std_val > 0 else 0
            is_z_outlier = abs(z_score) > 2.5

            if is_iqr_outlier or is_z_outlier:
                row = df.loc[idx]
                anomaly_item = {
                    "metric": metric,
                    "index": int(idx),
                    "value": round(float(val), 2),
                    "expected_range": f"{round(lower_bound, 2)} to {round(upper_bound, 2)}",
                    "z_score": round(float(z_score), 2),
                    "severity": "HIGH" if abs(z_score) > 3.0 else "MEDIUM"
                }

                if date_col and date_col in df.columns and pd.notna(row[date_col]):
                    anomaly_item["date"] = str(row[date_col])

                # Add dimension context if available
                context = []
                for col in ["Region", "Product", "Category", "Customer"]:
                    if col in df.columns and pd.notna(row[col]):
                        context.append(f"{col}: {row[col]}")
                    elif col.lower() in [c.lower() for c in df.columns]:
                        matched_c = [c for c in df.columns if c.lower() == col.lower()][0]
                        if pd.notna(row[matched_c]):
                            context.append(f"{matched_c}: {row[matched_c]}")

                anomaly_item["context"] = ", ".join(context) if context else "General"
                anomalies.append(anomaly_item)

                if len(anomalies) >= 10:  # Cap at top 10 anomalies
                    break

    return anomalies


def analyze_correlations(df: pd.DataFrame, numeric_cols: List[str]) -> List[Dict[str, Any]]:
    """
    Calculates pairwise Pearson correlations between numerical metrics.
    Filter for meaningful correlations (|r| >= 0.35).
    """
    correlations = []
    valid_cols = [c for c in numeric_cols if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]

    if len(valid_cols) < 2:
        return correlations

    corr_df = df[valid_cols].corr()

    for i in range(len(valid_cols)):
        for j in range(i + 1, len(valid_cols)):
            col1 = valid_cols[i]
            col2 = valid_cols[j]
            r = corr_df.loc[col1, col2]

            if not np.isnan(r) and abs(r) >= 0.35:
                direction = "positive" if r > 0 else "negative"
                strength = "strong" if abs(r) >= 0.7 else "moderate"
                correlations.append({
                    "col1": col1,
                    "col2": col2,
                    "correlation_r": round(float(r), 2),
                    "strength": strength,
                    "direction": direction,
                    "statement": f"Changes in {col1} show a {strength} {direction} correlation ({round(float(r), 2)}) associated with {col2}."
                })

    return correlations
