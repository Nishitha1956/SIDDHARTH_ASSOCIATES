# Siddharth Associates Assignment Reference Document

---

## 1. Objective

Build a complete **data pipeline** that takes raw international trade data (2017–Aug 2025) and turns it into **clean tables, analytical views, and interactive dashboards**.

By the end of this project, you should be able to:

- Parse messy **Goods Description** text into structured fields (model, capacity, material, price, etc.).
- Standardize units and compute additional fields such as **Grand Total** and **Landed Cost Per Unit**.
- Load the cleaned data into a **SQL database** and run queries for trends, Pareto analysis, and supplier insights.
- Build an interactive **Power BI or Tableau** dashboard to visualize macro trends, categories, supplier behavior, and unit economics.

This document guides you step by step, assuming you are a beginner who knows basic Python, SQL, and has seen Power BI/Tableau before.

---

## 2. Technical Requirements

### 2.1 Software

1. **Operating System**
    - Windows 10/11, macOS, or Linux.
2. **Python Environment**
    - Python 3.9+
    - Recommended: Anaconda or Miniconda (for easy environment and package management).
3. **Python Packages**
    - `pandas`
    - `numpy`
    - `sqlalchemy`
    - `psycopg2` or `mysqlclient` (depending on your DB)
    - `python-dotenv` (optional, for DB credentials)
    - `regex` or built-in `re`
    - Optional NLP helpers: `nltk` or `spacy` (only if you want more advanced text parsing).
4. **SQL Database**
    - Choose one:
        - PostgreSQL (recommended)
        - MySQL / MariaDB
        - SQL Server / SQLite (for practice)
5. **BI / Visualization Tool**
    - Power BI Desktop (Windows)
    - OR Tableau Public/Tableau Desktop.
6. **Editor / Notebook**
    - Jupyter Notebook / JupyterLab
    - OR VS Code (with Python extension).

### 2.2 Hardware

- Minimum 8 GB RAM (16 GB recommended if dataset is large).
- Enough disk space for:
    - Raw data (CSV/Excel)
    - Processed data
    - Database storage (a few GBs).

---

## 3. Step-by-Step Instructions

### Phase 0: Project Setup

1. **Create a project folder**
    - Example: `siddharth_trade_pipeline/`
2. **Create a Python virtual environment**
    - Using conda:
        
        ```bash
        conda create -n trade_env python=3.11
        conda activate trade_env
        
        ```
        
3. **Install required packages**
    
    ```bash
    pip install pandas numpy sqlalchemy psycopg2-binary python-dotenv regex
    
    ```
    
    > Adjust DB driver based on your chosen database.
    > 
4. **Set up version control (optional but recommended)**
    - Initialize a git repo:
        
        ```bash
        git init
        
        ```
        

---

### Phase 1: Understand & Inspect the Raw Data

1. **Place the raw dataset**
    - Save the provided CSV/Excel file in `data/raw/` (e.g., `data/raw/import_data_2017_2025.csv`).
2. **Open a Jupyter notebook**
    - Create `notebooks/01_data_inspection.ipynb`.
3. **Load and preview the data**
    - Check:
        - Column names match the schema.
        - Date format of **Date of Shipment**.
        - Range of years (2017–2025).
        - Sample values of **Goods Description**, **Unit**, **HSN Code**, etc.
4. **Identify data quality issues**
    - Missing values
    - Inconsistent units (`pcs`, `piece`, `nos`, etc.)
    - Strange or outlier values in **Duty Paid** / **Total Value (INR)**.

---

### Phase 2: Data Cleaning & Text Parsing (Python)

### 2A. Basic Cleaning

1. **Create a cleaning script**
    - Create `src/cleaning/clean_base.py`.
2. **Handle dates**
    - Convert `Date of Shipment` to a proper date type.
    - Derive **Year**, **Month**, **Quarter** for later analysis.
3. **Handle basic missing data**
    - Decide what to do with missing:
        - `Total Value (INR)`
        - `Duty Paid (INR)`
        - `Quantity`
    - Simple strategies for this assignment:
        - Drop rows with critical missing info.
        - Or fill with 0 for non-critical metrics (but document choices).

### 2B. Goods Description Parsing

1. **Create a parsing script**
    - File: `src/parsing/parse_goods_description.py`.
2. **Define the fields you want to extract**
    
    From `Goods Description`, extract:
    
    - `model_name`
    - `model_number`
    - `capacity_spec`
    - `material_type`
    - `embedded_quantity`
    - `unit_price_usd`
3. **Explore patterns manually**
    - Print a few sample descriptions.
    - Note common patterns like:
        - `"MODEL ABC-123 500ML BOROSILICATE GLASS @ USD 1.5/PC"`
        - `"WOODEN SPOON 10 INCH - PACK OF 50 - USD 0.2/PC"`
4. **Design regex/NLP rules**
    - Start simple:
        - Look for patterns containing `"USD"` or `"$/"`
        - Look for capacity patterns like `"500ML"`, `"1.5L"`, `"10 INCH"`.
        - Look for model-like tokens (`letters+digits`, e.g., `ABC-123`).
5. **Apply parsing to the entire column**
    - Use vectorized operations in pandas.
    - Store extracted values in new columns.

### 2C. Unit Standardization

1. **Create a unit mapping**
    - Decide a standard label (e.g., `PCS`, `KG`, `MT`).
    - Map variations (`nos`, `pieces`, `piece`, `pcs`) to a single value `PCS`.
2. **Apply mapping**
    - Add a new column `unit_standardized`.

---

### Phase 3: Feature Engineering (Python/Pandas)

1. **Create feature engineering script**
    - File: `src/feature_engineering/features.py`.
2. **Compute Grand Total**
    - `grand_total_inr = total_value_inr + duty_paid_inr`.
3. **Create Category & Sub-Category logic**
    - Use:
        - `HSN Code` ranges
        - Keywords in `Goods Description` and `HSN Description`.
    - Define rules such as:
        - If description contains `"GLASS"` → `Category = "Glass"`.
        - If glass description contains `"BOROSILICATE"` → `Sub-Category = "Borosilicate"`.
        - If description contains `"WOOD"` or `"WOODEN"` → `Category = "Wooden"`, etc.
4. **Calculate Landed Cost Per Unit**
    - `landed_cost_per_unit = grand_total_inr / quantity` (for valid quantity > 0).
5. **Export processed data**
    - Save as `data/processed/trade_cleaned.csv`.

---

### Phase 4: Load into SQL & Run Analyses

### 4A. Database Setup

1. **Create database**
    - Example (PostgreSQL):
        
        ```sql
        CREATE DATABASE trade_analysis;
        
        ```
        
2. **Design table schema**
    - Table `shipments` with columns:
        - Basic fields (date, year, month, etc.)
        - HSN-related fields
        - Parsed fields and engineered fields.
3. **Create table**
    - Use `CREATE TABLE` in an SQL file: `sql/schema.sql`.

### 4B. Load Data from Python

1. **Create DB loader script**
    - File: `src/db/load_to_db.py`.
    - Use `sqlalchemy` to connect and write the dataframe to the database.
2. **Verify in DB**
    - Run a simple `SELECT * FROM shipments LIMIT 10;` to confirm.

### 4C. SQL Analyses

1. **Macro Growth Trends (YoY)**
    - For each year, compute:
        - Total `Total Value (INR)`
        - Total `Duty Paid (INR)`
        - Total `Grand Total`
        - YoY % change.
2. **Pareto Analysis (Top 25 HSN Codes)**
    - Rank HSN codes by total value.
    - Calculate cumulative percentage.
    - Label top 25 individually and group the rest as `"Others"`.
3. **Supplier Logic**
    - Define "active in 2025":
        - Supplier with at least one shipment in year 2025.
    - Determine historical suppliers:
        - Those that had shipments in any year < 2025.
    - Determine "churned":
        - Suppliers who had shipments before 2025, but none in 2025.

---

### Phase 5: Micro-Level & Unit Economics

1. **Model-level analysis**
    - Group by `model_name`, `model_number`, and `year`.
    - Compute:
        - Total quantity purchased.
        - Average and median unit price.
2. **Supplier comparison**
    - For each model, compare:
        - Average `unit_price_inr` or `unit_price_usd` across suppliers.
3. **Capacity analysis**
    - Use `capacity_spec` to:
        - Aggregate total quantity per capacity.
        - Sort by highest volume capacities.
4. **Duty & cost anomalies**
    - Compute:
        - `duty_percentage = duty_paid_inr / total_value_inr`.
    - Flag rows where:
        - `duty_percentage` is way higher or lower than a typical range (e.g., > 2 standard deviations from the mean).

---

### Phase 6: Visualization & Reporting (Power BI / Tableau)

1. **Connect BI tool to database**
    - Use direct DB connection or import from CSV.
2. **Create Macro Dashboard**
    - Line chart:
        - X-axis: Year
        - Series: Sum of `Total Value (INR)`, `Duty Paid (INR)`, `Grand Total`.
    - YoY growth heatmap:
        - Rows: Year
        - Columns: Metric (Total Value, Duty Paid, Grand Total)
        - Color: YoY % change.
3. **Category Drill-Down**
    - Use a hierarchy:
        - Category → Sub-Category → Model.
    - Use Sunburst or TreeMap visualization.
4. **Supplier Analysis**
    - Bar chart:
        - X-axis: Supplier
        - Y-axis: Sum of `Grand Total`.
    - Status (Active / Churned):
        - Use a color or separate chart showing counts/values per status.
5. **Unit Economics**
    - Scatter plot:
        - X-axis: `capacity_spec` (numeric form if possible).
        - Y-axis: `landed_cost_per_unit`.
        - Color / shape: Category or Supplier.
6. **Export dashboard**
    - Save as `.pbix` or `.twb`.
    - Optionally export key views to PDF.

---

## 4. Project Structure

You can use this sample structure for your project:

```
siddharth_trade_pipeline/
├─ data/
│  ├─ raw/
│  │  └─ trade_data_2017_2025.csv
│  └─ processed/
│     └─ trade_cleaned.csv
├─ notebooks/
│  ├─ 01_data_inspection.ipynb
│  ├─ 02_parsing_and_cleaning.ipynb
│  └─ 03_feature_engineering.ipynb
├─ src/
│  ├─ parsing/
│  │  └─ parse_goods_description.py
│  ├─ cleaning/
│  │  └─ clean_base.py
│  ├─ feature_engineering/
│  │  └─ features.py
│  └─ db/
│     └─ load_to_db.py
├─ sql/
│  ├─ schema.sql
│  ├─ macro_trends.sql
│  ├─ pareto_hsn.sql
│  └─ supplier_analysis.sql
├─ dashboards/
│  ├─ trade_dashboard.pbix   (or .twb)
│  └─ exports/
│     └─ trade_dashboard.pdf
└─ docs/
   └─ assignment_reference.md  (this document)

```

- **`data/`**: Raw and processed datasets.
- **`notebooks/`**: Exploratory work and experimentation.
- **`src/`**: Reusable Python modules for pipeline steps.
- **`sql/`**: All SQL scripts (schema + analysis queries).
- **`dashboards/`**: Power BI/Tableau files and exports.
- **`docs/`**: Documentation and notes.

---

## 5. Example Codes

> These examples are illustrative and not full solutions. Adapt and extend them for your actual implementation.
> 

### 5.1 Loading and Basic Cleaning (Python)

```python
import pandas as pd

df = pd.read_csv("data/raw/trade_data_2017_2025.csv")

# Convert date column
df["date_of_shipment"] = pd.to_datetime(
    df["Date of Shipment"], format="%d/%m/%Y", errors="coerce"
)

# Derive year, month for analysis
df["year"] = df["date_of_shipment"].dt.year
df["month"] = df["date_of_shipment"].dt.month

```

---

### 5.2 Parsing Goods Description (Regex Skeleton)

```python
import re

def extract_unit_price_usd(description: str):
    """
    Example pattern: '... USD 1.5/PC', '... @ USD 2.00 PER PCS'
    Returns a float or None.
    """
    if not isinstance(description, str):
        return None

    pattern = r"USD\s*([\d\.]+)"
    match = re.search(pattern, description.upper())
    if match:
        return float(match.group(1))
    return None

df["unit_price_usd"] = df["Goods Description"].apply(extract_unit_price_usd)

```

You can create similar small functions for `model_number`, `capacity_spec`, etc., based on observed patterns.

---

### 5.3 Unit Standardization (Python)

```python
unit_map = {
    "PCS": "PCS", "PC": "PCS", "NOS": "PCS", "PIECES": "PCS",
    "KG": "KG", "KGS": "KG",
    "MT": "MT", "METRIC TON": "MT"
}

def normalize_unit(u):
    if not isinstance(u, str):
        return None
    u_upper = u.strip().upper()
    return unit_map.get(u_upper, u_upper)  # fallback: original

df["unit_standardized"] = df["Unit"].apply(normalize_unit)

```

---

### 5.4 Feature Engineering (Grand Total & Landed Cost)

```python
df["grand_total_inr"] = df["Total Value (INR)"] + df["Duty Paid (INR)"]

# Avoid division by zero
df["landed_cost_per_unit"] = df.apply(
    lambda row: row["grand_total_inr"] / row["Quantity"]
    if row["Quantity"] and row["Quantity"] > 0 else None,
    axis=1
)

```

---

### 5.5 Category & Sub-Category Assignment (Python Skeleton)

```python
def assign_category(row):
    desc = f"{row.get('Goods Description', '')} {row.get('HSN Description', '')}".upper()

    if "GLASS" in desc:
        return "Glass"
    if "WOOD" in desc or "WOODEN" in desc:
        return "Wooden"
    if "STEEL" in desc or "SS" in desc:
        return "Steel"
    # Add more rules...
    return "Others"

def assign_subcategory(row):
    cat = row["category"]
    desc = f"{row.get('Goods Description', '')} {row.get('HSN Description', '')}".upper()

    if cat == "Glass":
        if "BOROSILICATE" in desc:
            return "Borosilicate"
        if "OPAL" in desc or "OPALWARE" in desc:
            return "Opalware"
    if cat == "Wooden":
        if "SPOON" in desc:
            return "Spoon"
        if "FORK" in desc:
            return "Fork"
    return "Others"

df["category"] = df.apply(assign_category, axis=1)
df["sub_category"] = df.apply(assign_subcategory, axis=1)

```

---

### 5.6 Loading Data to SQL (Python + SQLAlchemy)

```python
from sqlalchemy import create_engine

# Example for PostgreSQL
engine = create_engine("postgresql+psycopg2://user:password@localhost/trade_analysis")

# Write to DB (you might specify 'if_exists' and chunksize)
df.to_sql("shipments", engine, if_exists="replace", index=False)

```

---

### 5.7 Macro Growth Trends (SQL Example)

```sql
-- Yearly totals and YoY growth for Total Value, Duty Paid, Grand Total
WITH yearly AS (
    SELECT
        year,
        SUM("Total Value (INR)")   AS total_value_inr,
        SUM("Duty Paid (INR)")     AS duty_paid_inr,
        SUM(grand_total_inr)       AS grand_total_inr
    FROM shipments
    GROUP BY year
)
SELECT
    year,
    total_value_inr,
    duty_paid_inr,
    grand_total_inr,
    100.0 * (total_value_inr - LAG(total_value_inr) OVER (ORDER BY year))
        / LAG(total_value_inr) OVER (ORDER BY year) AS yoy_total_value_pct,
    100.0 * (duty_paid_inr - LAG(duty_paid_inr) OVER (ORDER BY year))
        / LAG(duty_paid_inr) OVER (ORDER BY year) AS yoy_duty_paid_pct,
    100.0 * (grand_total_inr - LAG(grand_total_inr) OVER (ORDER BY year))
        / LAG(grand_total_inr) OVER (ORDER BY year) AS yoy_grand_total_pct
FROM yearly
ORDER BY year;

```

---

### 5.8 Pareto Analysis for HSN Codes (SQL Example)

```sql
WITH hsn_totals AS (
    SELECT
        "HSN Code" AS hsn_code,
        SUM("Total Value (INR)") AS total_value_inr
    FROM shipments
    GROUP BY "HSN Code"
),
sorted_hsn AS (
    SELECT
        hsn_code,
        total_value_inr,
        total_value_inr * 1.0 / SUM(total_value_inr) OVER () AS share_of_total,
        SUM(total_value_inr) OVER (ORDER BY total_value_inr DESC) * 1.0
          / SUM(total_value_inr) OVER () AS cumulative_share
    FROM hsn_totals
    ORDER BY total_value_inr DESC
)
SELECT *
FROM sorted_hsn
LIMIT 25;

```

You can extend this query to add an `"Others"` row grouping all remaining HSN codes.

---

### 5.9 Supplier Status (SQL Example)

```sql
-- Identify suppliers active in 2025
WITH supplier_years AS (
    SELECT DISTINCT supplier_name, year
    FROM shipments
)
SELECT
    s.supplier_name,
    CASE
        WHEN EXISTS (
            SELECT 1 FROM supplier_years sy
            WHERE sy.supplier_name = s.supplier_name
              AND sy.year = 2025
        ) THEN 'Active_2025'
        ELSE 'Not_Active_2025'
    END AS status_2025
FROM supplier_years s
GROUP BY s.supplier_name;

```

Extend this to label suppliers as **Active**, **Churned**, etc., based on their history.

---

### 5.10 Example DAX / Calculated Field Ideas (Power BI)

You won’t write full DAX here, but typical measures include:

- `Total Grand Total = SUM(shipments[grand_total_inr])`
- `Total Duty Paid = SUM(shipments[Duty Paid (INR)])`
- `YoY Grand Total = DIVIDE([Total Grand Total] - CALCULATE([Total Grand Total], DATEADD(Date[Date], -1, YEAR)), CALCULATE([Total Grand Total], DATEADD(Date[Date], -1, YEAR)))`

Use these measures in your trend lines and heatmaps.