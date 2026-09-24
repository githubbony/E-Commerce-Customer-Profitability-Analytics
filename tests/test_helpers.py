"""Tests for src.utils.helpers."""
import pandas as pd
import pytest

from src.utils.helpers import currency, pct, top_n


def test_currency_format():
    assert currency(1234.5) == "$1,234.50"
    assert currency(0) == "$0.00"


def test_pct_format():
    assert pct(0.25) == "25.0%"
    assert pct(0.1234, decimals=2) == "12.34%"


def test_top_n_returns_correct_rows():
    df = pd.DataFrame({"val": [3, 1, 4, 1, 5, 9, 2, 6]})
    result = top_n(df, "val", n=3)
    assert list(result["val"]) == [9, 6, 5]


def test_top_n_ascending():
    df = pd.DataFrame({"val": [3, 1, 4, 1, 5]})
    result = top_n(df, "val", n=2, ascending=True)
    assert list(result["val"]) == [1, 1]
