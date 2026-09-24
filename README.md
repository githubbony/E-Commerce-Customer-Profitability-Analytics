# E-Commerce Customer & Profitability Analytics

## Project Overview

This project analyzes e-commerce sales, profitability, customer purchasing behavior, products, regions, customer segments, and discount patterns using the Sample Superstore dataset.

The main business question is:

> **What factors influence sales, profitability, and customer purchasing behavior in an e-commerce business?**

The analysis was performed using Python, Pandas, Matplotlib, Jupyter Notebooks, and statistical/business analysis techniques.

## Objectives

* Analyze overall sales and profitability.
* Identify high-performing and low-performing product categories and sub-categories.
* Compare sales and profit across geographic regions.
* Analyze customer segment purchasing behavior.
* Examine the relationship between discounts and profitability.
* Identify the top and lowest-profit products.
* Generate business insights that can support better pricing, discount, product, and regional decisions.

## Dataset

The project uses the **Sample Superstore** dataset.

Dataset file:

`data/sample_-_superstore.xls`

The dataset is included in the project repository.

It contains information including:

* Order and shipping details
* Customer information
* Customer segments
* Geographic information
* Product categories and sub-categories
* Sales
* Quantity
* Discount
* Profit

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Jupyter Notebook
* Git & GitHub
* IBM Bob

## Project Structure

```text
E-Commerce-Customer-Profitability-Analytics/
│
├── data/
│   ├── processed/
│   ├── external/
│   ├── raw/
│   └── sample_-_superstore.xls
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_sales_and_profit.ipynb
│   ├── 03_category_and_product.ipynb
│   └── 04_regional_and_segments.ipynb
│
├── outputs/
│   ├── category_profit.png
│   ├── category_sales.png
│   ├── discount_vs_profit.png
│   ├── monthly_sales_profit.png
│   ├── regional_sales.png
│   ├── segment_profit.png
│   ├── segment_sales.png
│   └── top_10_products.png
│
├── src/
│   ├── analysis.py
│   ├── analysis/
│   ├── data/
│   ├── utils/
│   └── visualisation/
│
├── tests/
├── requirements.txt
├── pyproject.toml
├── AGENTS.md
└── README.md
```

## Setup and Installation

Clone the repository:

```bash
git clone https://github.com/githubbonny/E-Commerce-Customer-Profitability-Analytics.git
```

Move into the project directory:

```bash
cd E-Commerce-Customer-Profitability-Analytics
```

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

## Running the Analysis

Run the main analysis script:

```bash
python src/analysis.py
```

The analysis generates cleaned datasets and visualization files in the `data/processed/` and `outputs/` directories.

The Jupyter Notebooks in the `notebooks/` directory can also be used to review the analysis step by step.

## Key Results

The analysis produced the following overall business metrics:

* **Total Sales:** $2,326,534.35
* **Total Profit:** $292,296.81
* **Total Quantity Sold:** 38,654
* **Total Orders:** 5,111
* **Total Customers:** 804
* **Average Order Value:** $455.20
* **Overall Profit Margin:** 12.56%

### Category Performance

Technology generated the highest profit among the three major categories, while Furniture generated substantially lower profit relative to its sales volume.

### Regional Performance

The West region generated the highest sales and profit in the analyzed dataset.

### Customer Segments

The Consumer segment generated the highest sales and profit, followed by Corporate and Home Office.

### Discount and Profitability

The analysis shows a strong profitability concern at higher discount levels. Several high-discount groups recorded negative profit, indicating that aggressive discounting can reduce or eliminate profitability.

### Product Performance

The analysis identified products with both exceptionally high sales/profit and products generating significant losses. This provides opportunities for product-level pricing, promotion, and portfolio review.

## IBM Bob Usage

IBM Bob was used during the development of this project for project initialization, project structure generation, code scaffolding, and development assistance.

The project was initialized using IBM Bob, which generated the `AGENTS.md` project context file and the `.bob/` directory in the project root.

IBM Bob was also used to assist with the project scaffolding and analysis workflow.

IBM Bob documentation confirms that its `/init` process generates project-level `AGENTS.md` context and a `.bob` directory containing mode-specific context files.

## Project Outputs

The project produces:

* Cleaned datasets
* Monthly sales and profit analysis
* Category-level sales and profit analysis
* Regional analysis
* Customer segment analysis
* Discount versus profit analysis
* Top-product analysis
* Profitability analysis
* Data visualizations

## Author

**Ankitadhar**

## GitHub Repository

https://github.com/githubbonny/E-Commerce-Customer-Profitability-Analytics
