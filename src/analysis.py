import os
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# E-COMMERCE CUSTOMER & PROFITABILITY ANALYTICS
# ============================================================

# -----------------------------
# 1. Project paths
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# -----------------------------
# 2. Locate the Excel dataset
# -----------------------------

possible_files = [
    os.path.join(DATA_DIR, "sample_-_superstore.xls"),
    os.path.join(DATA_DIR, "sample_-_superstore.xlsx"),
    os.path.join(RAW_DIR, "sample_-_superstore.xls"),
    os.path.join(RAW_DIR, "sample_-_superstore.xlsx"),
]

DATA_FILE = None

for file_path in possible_files:
    if os.path.exists(file_path):
        DATA_FILE = file_path
        break

if DATA_FILE is None:
    print("ERROR: Sample Superstore Excel file was not found.")
    print("Please place the Excel file inside the data folder.")
    raise SystemExit(1)


# -----------------------------
# 3. Load dataset
# -----------------------------

print("=" * 60)
print("E-COMMERCE CUSTOMER & PROFITABILITY ANALYTICS")
print("=" * 60)

print("\nLoading dataset...")
print("File:", DATA_FILE)

df = pd.read_excel(DATA_FILE)

print("\nDataset loaded successfully.")
print("Rows:", len(df))
print("Columns:", list(df.columns))


# -----------------------------
# 4. Data cleaning
# -----------------------------

print("\n" + "=" * 60)
print("DATA CLEANING")
print("=" * 60)

# Remove completely empty rows
df = df.dropna(how="all")

# Remove duplicate rows
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

# Convert date columns
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

# Convert numeric columns
numeric_columns = [
    "Sales",
    "Quantity",
    "Discount",
    "Profit"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Remove rows without essential values
df = df.dropna(
    subset=[
        "Order ID",
        "Order Date",
        "Category",
        "Sales",
        "Profit"
    ]
)

# Create useful date fields
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

# Profit margin
df["Profit Margin (%)"] = (
    df["Profit"] / df["Sales"] * 100
)

# Replace infinite values
df["Profit Margin (%)"] = df["Profit Margin (%)"].replace(
    [float("inf"), float("-inf")],
    0
)

# Save cleaned dataset
cleaned_file = os.path.join(
    PROCESSED_DIR,
    "superstore_cleaned.csv"
)

df.to_csv(cleaned_file, index=False)

print("Duplicate rows removed:", duplicates)
print("Final rows:", len(df))
print("Cleaned dataset saved to:", cleaned_file)


# -----------------------------
# 5. Key business metrics
# -----------------------------

print("\n" + "=" * 60)
print("KEY BUSINESS METRICS")
print("=" * 60)

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_quantity = df["Quantity"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()
average_order_value = total_sales / total_orders
profit_margin = (total_profit / total_sales) * 100

print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Quantity Sold: {total_quantity:,}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Customers: {total_customers:,}")
print(f"Average Order Value: ${average_order_value:,.2f}")
print(f"Overall Profit Margin: {profit_margin:.2f}%")


# -----------------------------
# 6. Monthly performance
# -----------------------------

monthly = (
    df.groupby("Month")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

monthly["Month"] = pd.to_datetime(monthly["Month"])

monthly = monthly.sort_values(
    by="Month",
    ascending=True
)

print("\n" + "=" * 60)
print("MONTHLY PERFORMANCE")
print("=" * 60)

print(monthly.to_string(index=False))

plt.figure(figsize=(12, 6))

plt.plot(
    monthly["Month"],
    monthly["Sales"],
    marker="o",
    label="Sales"
)

plt.plot(
    monthly["Month"],
    monthly["Profit"],
    marker="o",
    label="Profit"
)

plt.title("Monthly Sales and Profit Trend")
plt.xlabel("Month")
plt.ylabel("Amount ($)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "monthly_sales_profit.png"
    ),
    dpi=300
)

plt.close()


# -----------------------------
# 7. Category performance
# -----------------------------

category = (
    df.groupby("Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

category = category.sort_values(
    by="Sales",
    ascending=False
)

print("\n" + "=" * 60)
print("CATEGORY PERFORMANCE")
print("=" * 60)

print(category.round(2).to_string(index=False))


# Sales by category
plt.figure(figsize=(9, 6))

plt.bar(
    category["Category"],
    category["Sales"]
)

plt.title("Sales by Product Category")
plt.xlabel("Category")
plt.ylabel("Sales ($)")
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "category_sales.png"
    ),
    dpi=300
)

plt.close()


# Profit by category
plt.figure(figsize=(9, 6))

plt.bar(
    category["Category"],
    category["Profit"]
)

plt.title("Profit by Product Category")
plt.xlabel("Category")
plt.ylabel("Profit ($)")
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "category_profit.png"
    ),
    dpi=300
)

plt.close()


# -----------------------------
# 8. Sub-category performance
# -----------------------------

subcategory = (
    df.groupby("Sub-Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

subcategory = subcategory.sort_values(
    by="Profit",
    ascending=False
)

print("\n" + "=" * 60)
print("TOP SUB-CATEGORIES BY PROFIT")
print("=" * 60)

print(
    subcategory.head(10)
    .round(2)
    .to_string(index=False)
)


# -----------------------------
# 9. Regional performance
# -----------------------------

region = (
    df.groupby("Region")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

region = region.sort_values(
    by="Sales",
    ascending=False
)

print("\n" + "=" * 60)
print("REGIONAL PERFORMANCE")
print("=" * 60)

print(region.round(2).to_string(index=False))


plt.figure(figsize=(9, 6))

plt.bar(
    region["Region"],
    region["Sales"]
)

plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales ($)")
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "regional_sales.png"
    ),
    dpi=300
)

plt.close()


# -----------------------------
# 10. Customer segment analysis
# -----------------------------

segment = (
    df.groupby("Segment")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Customers=("Customer ID", "nunique"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

segment = segment.sort_values(
    by="Sales",
    ascending=False
)

print("\n" + "=" * 60)
print("CUSTOMER SEGMENT PERFORMANCE")
print("=" * 60)

print(segment.round(2).to_string(index=False))


# Segment sales
plt.figure(figsize=(9, 6))

plt.bar(
    segment["Segment"],
    segment["Sales"]
)

plt.title("Sales by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Sales ($)")
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "segment_sales.png"
    ),
    dpi=300
)

plt.close()


# Segment profit
plt.figure(figsize=(9, 6))

plt.bar(
    segment["Segment"],
    segment["Profit"]
)

plt.title("Profit by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Profit ($)")
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "segment_profit.png"
    ),
    dpi=300
)

plt.close()


# -----------------------------
# 11. Discount vs Profit
# -----------------------------

discount_analysis = (
    df.groupby("Discount")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

discount_analysis = discount_analysis.sort_values(
    by="Discount",
    ascending=True
)

print("\n" + "=" * 60)
print("DISCOUNT VS PROFIT")
print("=" * 60)

print(
    discount_analysis
    .round(2)
    .to_string(index=False)
)


plt.figure(figsize=(10, 6))

plt.scatter(
    df["Discount"],
    df["Profit"],
    alpha=0.4
)

plt.title("Discount vs Profit")
plt.xlabel("Discount")
plt.ylabel("Profit ($)")
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "discount_vs_profit.png"
    ),
    dpi=300
)

plt.close()


# -----------------------------
# 12. Top products
# -----------------------------

top_products = (
    df.groupby(
        ["Product ID", "Product Name"]
    )
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

top_products = top_products.sort_values(
    by="Sales",
    ascending=False
)

print("\n" + "=" * 60)
print("TOP 10 PRODUCTS BY SALES")
print("=" * 60)

print(
    top_products.head(10)
    .round(2)
    .to_string(index=False)
)


top10 = top_products.head(10).copy()

# Shorten product names for chart readability
top10["Short Name"] = (
    top10["Product Name"]
    .str.slice(0, 35)
)

plt.figure(figsize=(12, 7))

plt.barh(
    top10["Short Name"],
    top10["Sales"]
)

plt.title("Top 10 Products by Sales")
plt.xlabel("Sales ($)")
plt.ylabel("Product")
plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "top_10_products.png"
    ),
    dpi=300
)

plt.close()


# -----------------------------
# 13. Top profitable products
# -----------------------------

top_profit_products = top_products.sort_values(
    by="Profit",
    ascending=False
)

print("\n" + "=" * 60)
print("TOP 10 PRODUCTS BY PROFIT")
print("=" * 60)

print(
    top_profit_products.head(10)
    .round(2)
    .to_string(index=False)
)


# -----------------------------
# 14. Negative-profit products
# -----------------------------

loss_products = (
    df.groupby(
        ["Product ID", "Product Name"]
    )
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

loss_products = loss_products.sort_values(
    by="Profit",
    ascending=True
)

print("\n" + "=" * 60)
print("10 PRODUCTS WITH LOWEST PROFIT")
print("=" * 60)

print(
    loss_products.head(10)
    .round(2)
    .to_string(index=False)
)


# -----------------------------
# 15. Export summary tables
# -----------------------------

category.to_csv(
    os.path.join(
        PROCESSED_DIR,
        "category_performance.csv"
    ),
    index=False
)

region.to_csv(
    os.path.join(
        PROCESSED_DIR,
        "regional_performance.csv"
    ),
    index=False
)

segment.to_csv(
    os.path.join(
        PROCESSED_DIR,
        "segment_performance.csv"
    ),
    index=False
)

monthly.to_csv(
    os.path.join(
        PROCESSED_DIR,
        "monthly_performance.csv"
    ),
    index=False
)

top_products.to_csv(
    os.path.join(
        PROCESSED_DIR,
        "product_performance.csv"
    ),
    index=False
)


# -----------------------------
# 16. Final summary
# -----------------------------

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)

print("\nCleaned dataset:")
print(cleaned_file)

print("\nCharts generated:")

chart_files = [
    "monthly_sales_profit.png",
    "category_sales.png",
    "category_profit.png",
    "regional_sales.png",
    "segment_sales.png",
    "segment_profit.png",
    "discount_vs_profit.png",
    "top_10_products.png"
]

for chart in chart_files:
    print("-", chart)

print("\nOutput directory:")
print(OUTPUT_DIR)

print("\nProject analysis finished successfully.")