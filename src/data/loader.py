"""Data ingestion and cleaning utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


DATA_RAW = Path(__file__).resolve().parents[2] / "data" / "raw"
DATA_PROCESSED = Path(__file__).resolve().parents[2] / "data" / "processed"


def load_raw(filename: str) -> pd.DataFrame:
    """Load a raw CSV or Excel file from data/raw/.

    Args:
        filename: File name including extension (e.g. ``"orders.csv"``).

    Returns:
        Loaded DataFrame with basic dtype coercions applied.
    """
    path = DATA_RAW / filename
    if path.suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)
    return _apply_base_dtypes(df)


def _apply_base_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce known column patterns to correct dtypes."""
    date_cols = [c for c in df.columns if "date" in c.lower()]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")

    # Normalise column names: snake_case, no spaces
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[\s\-]+", "_", regex=True)
        .str.replace(r"[^\w]", "", regex=True)
    )
    return df


def save_processed(df: pd.DataFrame, filename: str) -> Path:
    """Persist a cleaned DataFrame to data/processed/ as Parquet.

    Args:
        df: Cleaned DataFrame.
        filename: Output filename *without* extension.

    Returns:
        Absolute path of the saved file.
    """
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = DATA_PROCESSED / f"{filename}.parquet"
    df.to_parquet(out, index=False)
    return out
