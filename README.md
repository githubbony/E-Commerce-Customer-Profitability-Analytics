# E-Commerce Customer & Profitability Analytics

A Python data analytics project examining e-commerce sales trends, category and product performance, the relationship between discounting and profit, regional performance, and customer segment behaviour.

## Project Structure

```
├── data/
│   ├── raw/          # Source data files (not committed)
│   ├── processed/    # Cleaned, feature-engineered datasets
│   └── external/     # Reference/lookup tables
├── notebooks/
│   ├── 01_data_cleaning.ipynb           # Load, clean, derive base metrics
│   ├── 02_sales_and_profit.ipynb        # Sales trends + discount vs. profit
│   ├── 03_category_and_product.ipynb    # Category/sub-category + top/bottom products
│   └── 04_regional_and_segments.ipynb  # Regional performance + customer segments
├── src/
│   ├── __init__.py
│   ├── data/         # Ingestion & cleaning helpers
│   ├── analysis/     # Core analytics logic
│   ├── visualisation/# Chart builders
│   └── utils/        # Shared utilities
├── tests/            # pytest test suite
├── outputs/
│   ├── figures/      # Saved charts
│   └── reports/      # HTML / PDF reports
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Quick Start

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch JupyterLab
jupyter lab

# 4. Run tests
pytest

# 5. Lint & format
ruff check src tests
black src tests
```

## Analysis Scope

| Domain | Key Questions |
|---|---|
| **Sales Trends** | Monthly/yearly revenue trajectory; seasonality patterns |
| **Category & Product Performance** | Which categories and sub-categories drive sales vs. profit; top and bottom 10 products |
| **Discount vs. Profit** | Does discounting grow revenue or erode margin? At what threshold do orders become loss-making? |
| **Regional Performance** | Sales and profit by region and state; which geographies over/under-perform |
| **Customer Segments** | Revenue, profit, and margin profile of Consumer, Corporate, and Home Office segments |

## Data Conventions

- All monetary columns in **USD**.
- Discount is a **ratio** (0.0–1.0), not a percentage.
- `profit_margin = profit / sales` (can be negative).
- Dates parsed as `pd.Timestamp`; timezone-naive.
