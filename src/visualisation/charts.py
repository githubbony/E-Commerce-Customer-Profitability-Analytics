"""Reusable chart builders using matplotlib / seaborn / plotly."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


FIGURES_DIR = Path(__file__).resolve().parents[2] / "outputs" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# House palette (matches README colour scheme)
PALETTE = "Blues_r"


def bar_profitability(
    df: pd.DataFrame,
    x: str,
    y: str = "total_profit",
    title: str = "Profitability",
    save_as: Optional[str] = None,
) -> plt.Figure:
    """Horizontal bar chart for profit by category/segment/region.

    Args:
        df: Aggregated DataFrame (output of :func:`~src.analysis.profitability.segment_profitability`).
        x: Column to plot on x-axis (profit values).
        y: Column for category labels.
        title: Chart title.
        save_as: Filename (without extension) to save in ``outputs/figures/``.

    Returns:
        Matplotlib Figure.
    """
    fig, ax = plt.subplots(figsize=(10, max(4, len(df) * 0.5)))
    sns.barplot(data=df, x=x, y=y, palette=PALETTE, ax=ax)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(x.replace("_", " ").title())
    ax.set_ylabel(y.replace("_", " ").title())
    plt.tight_layout()
    if save_as:
        fig.savefig(FIGURES_DIR / f"{save_as}.png", dpi=150)
    return fig


def margin_heatmap(
    df: pd.DataFrame,
    index: str,
    columns: str,
    values: str = "avg_margin",
    title: str = "Profit Margin Heatmap",
    save_as: Optional[str] = None,
) -> plt.Figure:
    """Pivot-based heatmap of profit margins.

    Args:
        df: Aggregated DataFrame.
        index: Row dimension column.
        columns: Column dimension.
        values: Metric to display.
        title: Chart title.
        save_as: Optional filename stem for saving.

    Returns:
        Matplotlib Figure.
    """
    pivot = df.pivot(index=index, columns=columns, values=values)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot, annot=True, fmt=".1%", cmap="RdYlGn", center=0, ax=ax)
    ax.set_title(title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    if save_as:
        fig.savefig(FIGURES_DIR / f"{save_as}.png", dpi=150)
    return fig
