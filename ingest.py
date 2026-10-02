import io
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any

def load_dataset(file_bytes: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Safely reads CSV or Excel file bytes into a clean pandas DataFrame.
    Returns (df, metadata_dict).
    """
    metadata = {
        "filename": filename,
        "warnings": [],
        "original_rows": 0,
        "original_cols": 0
    }
    
    filename_lower = filename.lower()
    try:
        if filename_lower.endswith(".csv"):
            # Try utf-8 first, fallback to latin-1
            try:
                df = pd.read_csv(io.BytesIO(file_bytes), encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(io.BytesIO(file_bytes), encoding="latin-1")
        elif filename_lower.endswith((".xlsx", ".xls")):
            df = pd.read_excel(io.BytesIO(file_bytes))
        else:
            # Default to csv attempt
            df = pd.read_csv(io.BytesIO(file_bytes))
    except Exception as e:
        raise ValueError(f"Could not parse file '{filename}': {str(e)}")

    if df.empty:
        raise ValueError("Uploaded dataset is empty (0 rows).")

    metadata["original_rows"] = len(df)
    metadata["original_cols"] = len(df.columns)

    # Clean column names (strip whitespace, sanitize)
    df.columns = [str(c).strip() for c in df.columns]

    # Replace common null representations
    df = df.replace(["", " ", "NA", "N/A", "null", "NULL", "None", "none", "-", "NaN"], np.nan)

    # Check for empty columns
    empty_cols = [c for c in df.columns if df[c].dropna().empty]
    if empty_cols:
        metadata["warnings"].append(f"Columns with 100% missing values detected: {', '.join(empty_cols)}")

    # Check for duplicate rows
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        metadata["warnings"].append(f"Dataset contains {dup_count} duplicate row(s).")

    return df, metadata
