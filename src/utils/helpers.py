"""Shared utility functions."""
from __future__ import annotations

import pandas as pd


def currency(value: float) -> str:
    """Format a float as a USD currency string."""
    return f"${value:,.2f}"


def pct(value: float, decimals: int = 1) -> str:
    """Format a float ratio as a percentage string (0.25 → '25.0%')."""
    return f"{value * 100:.{decimals}f}%"


def top_n(
    df: pd.DataFrame,
    column: str,
    n: int = 10,
    ascending: bool = False,
) -> pd.DataFrame:
    """Return the top-N rows sorted by *column*.

    Args:
        df: Input DataFrame.
        column: Column to sort by.
        n: Number of rows to return.
        ascending: Sort direction.

    Returns:
        Sliced and sorted DataFrame.
    """
    return df.sort_values(column, ascending=ascending).head(n)
