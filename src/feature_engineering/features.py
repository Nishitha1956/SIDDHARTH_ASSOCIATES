import pandas as pd
from pathlib import Path
import numpy as np

# Correct Excel path
input_file = Path(__file__).resolve().parents[2] / "data" / "raw" / "trade_data_2017_2025.xlsx"

print(f"Loading Excel file: {input_file}")

# Load XLSX file
df = pd.read_excel(input_file)
print("Loaded", len(df), "rows and", len(df.columns), "columns.")

# Convert numeric fields correctly
df["TOTAL VALUE_INR"] = pd.to_numeric(df["TOTAL VALUE_INR"], errors="coerce")
df["DUTY PAID_INR"] = pd.to_numeric(df["DUTY PAID_INR"], errors="coerce")
df["QUANTITY"] = pd.to_numeric(df["QUANTITY"], errors="coerce")

# Replace NaN with 0 for safety
df["TOTAL VALUE_INR"].fillna(0, inplace=True)
df["DUTY PAID_INR"].fillna(0, inplace=True)

# 1. Grand Total (INR)
df["grand_total_inr"] = df["TOTAL VALUE_INR"] + df["DUTY PAID_INR"]

# 2. Landed cost per unit
def compute_landed_cost(row):
    qty = row["QUANTITY"]
    if pd.isna(qty) or qty <= 0:
        return None
    return row["grand_total_inr"] / qty

df["landed_cost_per_unit"] = df.apply(compute_landed_cost, axis=1)

# Save processed output XLSX
output_file = Path(__file__).resolve().parents[2] / "data" / "processed" / "trade_cleaned_costs.xlsx"
df.to_excel(output_file, index=False)

print("Cost fields calculated & saved successfully!")
print("Output file:", output_file)
