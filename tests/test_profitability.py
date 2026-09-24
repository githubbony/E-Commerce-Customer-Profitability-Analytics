"""Tests for src.analysis.profitability."""
import pandas as pd
import numpy as np
import pytest

from src.analysis.profitability import (
    add_profit_metrics,
    segment_profitability,
    discount_impact,
    rfm_scores,
)


@pytest.fixture
def sample_orders() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": ["O1", "O2", "O3", "O4", "O5"],
            "customer_id": ["C1", "C2", "C1", "C3", "C2"],
            "order_date": pd.to_datetime(
                ["2023-01-10", "2023-02-15", "2023-03-20", "2023-04-05", "2023-05-01"]
            ),
            "sales": [100.0, 200.0, 150.0, 50.0, 300.0],
            "profit": [20.0, -10.0, 30.0, 5.0, 60.0],
            "discount": [0.0, 0.20, 0.10, 0.0, 0.15],
            "quantity": [2, 4, 3, 1, 6],
            "segment": ["Consumer", "Corporate", "Consumer", "Home Office", "Corporate"],
            "region": ["West", "East", "West", "Central", "East"],
        }
    )


class TestAddProfitMetrics:
    def test_margin_computed(self, sample_orders):
        df = add_profit_metrics(sample_orders)
        assert "profit_margin" in df.columns
        assert round(df.loc[0, "profit_margin"], 2) == 0.20

    def test_no_division_by_zero(self):
        df = pd.DataFrame({"sales": [0.0], "profit": [0.0], "discount": [0.0], "quantity": [1]})
        result = add_profit_metrics(df)
        assert pd.isna(result.loc[0, "profit_margin"])

    def test_discount_pct(self, sample_orders):
        df = add_profit_metrics(sample_orders)
        assert df["discount_pct"].max() == pytest.approx(20.0)


class TestSegmentProfitability:
    def test_returns_sorted_by_profit(self, sample_orders):
        df = add_profit_metrics(sample_orders)
        result = segment_profitability(df, "segment")
        profits = result["total_profit"].tolist()
        assert profits == sorted(profits, reverse=True)

    def test_aggregates_correctly(self, sample_orders):
        df = add_profit_metrics(sample_orders)
        result = segment_profitability(df, "region")
        west = result.loc[result["region"] == "West", "total_profit"].values[0]
        assert west == pytest.approx(50.0)  # 20 + 30


class TestDiscountImpact:
    def test_tier_columns_present(self, sample_orders):
        result = discount_impact(sample_orders)
        assert "discount_tier" in result.columns

    def test_zero_discount_tier_exists(self, sample_orders):
        result = discount_impact(sample_orders)
        assert "0%" in result["discount_tier"].values


class TestRfmScores:
    def test_rfm_score_range(self, sample_orders):
        result = rfm_scores(sample_orders, snapshot_date=pd.Timestamp("2023-06-01"))
        assert result["rfm_score"].between(3, 15).all()

    def test_one_row_per_customer(self, sample_orders):
        result = rfm_scores(sample_orders)
        assert len(result) == sample_orders["customer_id"].nunique()
