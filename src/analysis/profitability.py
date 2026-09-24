"""Core profitability and sales analysis functions."""
from __future__ import annotations

import pandas as pd
import numpy as np


def add_profit_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived profit metrics to a sales DataFrame.

    Expects columns: ``sales``, ``profit``, ``discount``, ``quantity``.

    Adds:
        - ``profit_margin``: profit / sales (NaN where sales == 0)
        - ``revenue_per_unit``: sales / quantity
        - ``discount_pct``: discount * 100
    """
    df = df.copy()
    df["profit_margin"] = df["profit"] / df["sales"].replace(0, pd.NA)
    df["revenue_per_unit"] = df["sales"] / df["quantity"].replace(0, pd.NA)
    df["discount_pct"] = df["discount"] * 100
    return df


def segment_profitability(df: pd.DataFrame, group_by: str | list[str]) -> pd.DataFrame:
    """Aggregate profit KPIs by a grouping dimension.

    Args:
        df: Sales DataFrame with profit metrics already added.
        group_by: Column name(s) to group by.

    Returns:
        Aggregated DataFrame sorted by ``total_profit`` descending.
    """
    agg = (
        df.groupby(group_by)
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            avg_margin=("profit_margin", "mean"),
            avg_discount=("discount", "mean"),
            order_count=("sales", "count"),
        )
        .reset_index()
        .sort_values("total_profit", ascending=False)
    )
    return agg


def discount_impact(df: pd.DataFrame) -> pd.DataFrame:
    """Bucket orders by discount tier and compute profit impact.

    Discount tiers: 0%, 1-10%, 11-20%, 21-30%, >30%.
    """
    bins = [-0.001, 0.0, 0.10, 0.20, 0.30, 1.0]
    labels = ["0%", "1-10%", "11-20%", "21-30%", ">30%"]
    df = df.copy()
    df["discount_tier"] = pd.cut(df["discount"], bins=bins, labels=labels)
    return segment_profitability(df, "discount_tier")


def rfm_scores(
    df: pd.DataFrame,
    customer_col: str = "customer_id",
    date_col: str = "order_date",
    revenue_col: str = "sales",
    snapshot_date: pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Compute RFM (Recency, Frequency, Monetary) scores per customer.

    Args:
        df: Transaction-level DataFrame.
        customer_col: Column identifying each customer.
        date_col: Column with order dates (must be datetime).
        revenue_col: Column with order revenue.
        snapshot_date: Reference date for recency. Defaults to max order date + 1 day.

    Returns:
        DataFrame with columns: customer_id, recency_days, frequency, monetary,
        r_score, f_score, m_score, rfm_score (1–5 quintiles each).
    """
    if snapshot_date is None:
        snapshot_date = df[date_col].max() + pd.Timedelta(days=1)

    rfm = (
        df.groupby(customer_col)
        .agg(
            recency_days=(date_col, lambda x: (snapshot_date - x.max()).days),
            frequency=(date_col, "count"),
            monetary=(revenue_col, "sum"),
        )
        .reset_index()
    )

    rfm["r_score"] = pd.qcut(rfm["recency_days"], q=5, labels=[5, 4, 3, 2, 1])
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5])
    rfm["m_score"] = pd.qcut(rfm["monetary"], q=5, labels=[1, 2, 3, 4, 5])
    rfm["rfm_score"] = (
        rfm["r_score"].astype(int)
        + rfm["f_score"].astype(int)
        + rfm["m_score"].astype(int)
    )
    return rfm
