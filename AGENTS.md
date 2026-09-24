# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project

**E-Commerce Customer & Profitability Analytics** — Python data analytics project with a confirmed scope of five domains: **sales trends**, **category & product performance**, **discount vs. profit**, **regional performance**, and **customer segments** (Consumer / Corporate / Home Office).

**4-notebook structure:**
- `01_data_cleaning.ipynb` — load, clean, derive base metrics
- `02_sales_and_profit.ipynb` — sales trends + discount vs. profit
- `03_category_and_product.ipynb` — category/sub-category + top/bottom products
- `04_regional_and_segments.ipynb` — regional performance + customer segments

## Commands

```bash
# Install
pip install -r requirements.txt

# Run tests (all)
pytest

# Run a single test file
pytest tests/test_profitability.py -v

# Run a single test by name
pytest tests/test_profitability.py::TestRfmScores::test_rfm_score_range -v

# Lint
ruff check src tests

# Format
black src tests
```

## Project-Specific Conventions

### Data column naming
- Raw files loaded via [`load_raw()`](src/data/loader.py) auto-normalise column names to **snake_case** (spaces/hyphens → `_`, special chars stripped). Expect `order_id`, `ship_date`, etc. — never `Order ID` or `Order-ID`.
- `discount` is always a **ratio** (0.0–1.0), never a percentage. `discount_pct = discount * 100`.
- `profit_margin = profit / sales` — can be negative; columns with `sales == 0` produce `NaN` (not 0).

### Analysis flow
1. Raw → [`src/data/loader.py`](src/data/loader.py) → `data/processed/*.parquet`
2. Metrics → [`src/analysis/profitability.py`](src/analysis/profitability.py) (`add_profit_metrics` first, then aggregation functions)
3. Charts → [`src/visualisation/charts.py`](src/visualisation/charts.py) (auto-saves PNGs to `outputs/figures/` when `save_as` is set)

### Key functions
- [`add_profit_metrics(df)`](src/analysis/profitability.py) — **must be called before** any aggregation; adds `profit_margin`, `revenue_per_unit`, `discount_pct`.
- [`segment_profitability(df, group_by)`](src/analysis/profitability.py) — `group_by` accepts a string or list; returns sorted by `total_profit` desc.
- [`rfm_scores(df)`](src/analysis/profitability.py) — scores are quintile-based (1–5 each), `rfm_score` range is 3–15.
- [`top_n(df, column, n)`](src/utils/helpers.py) — thin wrapper, not pandas `.nlargest()` (preserves original index order within top-N).

### Processed data format
Processed files are **Parquet** (not CSV). Load with `pd.read_parquet(DATA_PROCESSED / 'filename.parquet')`. `DATA_PROCESSED` is exported from [`src/data/loader.py`](src/data/loader.py).

### Testing
- Tests live in `tests/`, co-located with `src/` (not inside `src/`).
- `pyproject.toml` configures `pytest` to auto-run coverage (`--cov=src`); no need to pass flags manually.
- Fixtures producing synthetic DataFrames should include all columns that `add_profit_metrics` expects: `sales`, `profit`, `discount`, `quantity`.

## Code Style
- **Line length**: 88 (Black default). `ruff` ignores E501.
- **Imports**: `from __future__ import annotations` at top of every `src/` module. stdlib → third-party → `src` (enforced by `ruff isort`).
- **Types**: Use `pd.DataFrame`, `pd.Timestamp`, `str | list[str]` union syntax (Python 3.10+). Avoid `Optional[X]`; use `X | None`.
- **Docstrings**: Google style. All public functions in `src/` must have Args/Returns sections.
- **No raw SQL**: All data access goes through pandas / Parquet. No database connections in this project.
