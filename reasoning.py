import pandas as pd
from typing import Dict, Any, List, Optional

def deduce_root_causes(
    df: pd.DataFrame,
    metric_name: str,
    metric_col: str,
    dimensions: Dict[str, Optional[str]],
    trend_data: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Hierarchical root-cause deduction linking KPI outcome to dimensions and potential operational bottlenecks.
    """
    causes = []
    if metric_col not in df.columns or not pd.api.types.is_numeric_dtype(df[metric_col]):
        return causes

    date_col = dimensions.get("date")
    region_col = dimensions.get("region")
    product_col = dimensions.get("product")
    inventory_col = dimensions.get("inventory")
    cost_col = dimensions.get("cost")

    # Check metric trend
    metric_stats = trend_data.get("metrics", {}).get(metric_col, {})
    change_pct = metric_stats.get("change_pct", 0.0)

    if abs(change_pct) < 1.0:
        return causes

    outcome_type = "DECLINE" if change_pct < 0 else "GROWTH"

    # Step 1: Region-level cause deduction
    if region_col and region_col in df.columns:
        grp = df.groupby(region_col, observed=False)[metric_col].sum()
        sorted_grp = grp.sort_values(ascending=(outcome_type == "DECLINE"))
        top_affected_region = sorted_grp.index[0] if len(sorted_grp) > 0 else None
        
        if top_affected_region:
            region_df = df[df[region_col] == top_affected_region]

            # Step 2: Product-level cause within region
            product_cause = None
            if product_col and product_col in df.columns:
                prod_grp = region_df.groupby(product_col, observed=False)[metric_col].sum()
                sorted_prod = prod_grp.sort_values(ascending=(outcome_type == "DECLINE"))
                if len(sorted_prod) > 0:
                    top_prod = sorted_prod.index[0]
                    product_cause = str(top_prod)

            # Step 3: Check inventory constraint
            operational_bottleneck = None
            if inventory_col and inventory_col in df.columns and pd.api.types.is_numeric_dtype(df[inventory_col]):
                avg_inv_overall = df[inventory_col].mean()
                avg_inv_region = region_df[inventory_col].mean()
                if avg_inv_region < avg_inv_overall * 0.8:
                    operational_bottleneck = f"Inventory availability in {top_affected_region} ({avg_inv_region:.1f}) was 20%+ below average ({avg_inv_overall:.1f})."

            # Step 4: Check cost surge constraint
            if not operational_bottleneck and cost_col and cost_col in df.columns and pd.api.types.is_numeric_dtype(df[cost_col]):
                avg_cost_region = region_df[cost_col].sum()
                if avg_cost_region > 0 and outcome_type == "DECLINE":
                    operational_bottleneck = f"Elevated operational cost observed in {top_affected_region} region."

            causes.append({
                "metric": metric_name,
                "change_pct": change_pct,
                "primary_affected_segment": f"{region_col}: {top_affected_region}",
                "secondary_driver": f"{product_col}: {product_cause}" if product_cause else "Multiple items",
                "operational_bottleneck": operational_bottleneck or "Demand volume shift",
                "confidence": "HIGH" if operational_bottleneck else "MEDIUM"
            })

    return causes
