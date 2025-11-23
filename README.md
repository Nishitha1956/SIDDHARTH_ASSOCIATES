📦 International Trade Data Analysis & End-to-End Data Pipeline
(Siddharth Associates – 2017 to 2025 Import Data)

This project builds a complete data engineering and analytics pipeline for processing international import trade data (2017–2025).
The organization currently receives raw data from trade data providers (Seair/Eximpedia), and the goal is to automate the entire workflow—from raw Excel files to dashboards and insights.

The final pipeline cleans, transforms, loads, and visualizes trade data, enabling the company to make better business decisions.

🚀 Project Objectives

Convert raw, messy Excel data into a clean, structured dataset.

Parse unstructured fields like Goods Description to extract useful attributes (model, material, capacity, etc.).

Standardize all units, compute financial metrics, and generate additional derived fields.

Load processed data into a SQL database.

Build analytical reports and dashboards using Power BI.

Automate the pipeline to ensure repeatable, reliable analysis.

🛠️ Tech Stack

Python – Data cleaning, transformations, parsing

Pandas / NumPy – Data preprocessing

Regex – Goods description parsing

MySQL – Data warehouse & analytical storage

Power BI – Interactive dashboards

Excel/CSV – Input and intermediate files

GitHub – Version control & documentation

📂 Pipeline Stages
1. Data Ingestion

Import raw Excel files (2017–Aug 2025).

Standardize column names.

Remove duplicates & blank rows.

Save intermediate output as cleaned CSV.

2. Data Cleaning & Transformation (Python)

Remove noise characters and unnecessary spacing.

Extract structured fields from “Goods Description”, such as:

Model / Model No

Material

Capacity

Wattage

Size

Brand

Convert units (KG/MT/Units).

Convert all currency values to INR if applicable.

Compute new metrics:

Grand Total (Value + Duty)

Landed Cost Per Unit

Per-Unit Price

Total Duty %

Save processed dataset.

3. Loading into SQL Database

Create database: trade_analysis

Create table: shipments

Load processed CSV into SQL using a Python script.

Verify row count, data integrity, and indexing.

Enable analytics queries.

4. Power BI Dashboard Development

Four dashboards created:

a) Macro Trends Dashboard

Yearly import value

Monthly trend

Duty impact

YoY comparison

b) Category / Subcategory Analysis

Product category contribution

Subcategory drilldown

Model-level performance

c) Supplier Analytics

Top suppliers

Supplier share

Active vs inactive suppliers

d) Unit Economics Dashboard

Landed cost per model

Capacity vs cost scatter

Quantity vs cost distribution

Includes slicers for:

Year, category, supplier, country, HSN code, etc.

📊 Key Insights Enabled

Track import trends from 2017–2025.

Identify high-performing categories and models.

Understand cost structures and margin drivers.

Monitor supplier contribution and dependency.

Support strategic sourcing & procurement decisions.

📁 Repository Structure
├── data/
│   ├── raw/                # Raw Excel files (2017–2025)
│   ├── processed/          # Cleaned & transformed files
│
├── scripts/
│   ├── data_cleaning.ipynb
│   ├── goods_parser.py
│   ├── load_to_mysql.py
│
├── sql/
│   ├── create_tables.sql
│   ├── analysis_queries.sql
│
├── dashboard/
│   ├── trade_dashboard.pbix
│
└── README.md               # Project documentation

✔️ Final Deliverables

Cleaned dataset (trade_cleaned.csv)

SQL database with analytical tables

Python scripts for the pipeline

Power BI dashboard with 4 analytical modules

Project documentation (this README)
