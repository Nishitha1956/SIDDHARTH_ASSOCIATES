import pandas as pd
from pathlib import Path

file_path = Path("../../data/raw/trade_data_2017_2025.xlsx")

df = pd.read_excel(file_path)

# Use the actual column name: "DATE"
df["date_of_shipment"] = pd.to_datetime(
    df["DATE"],
    dayfirst=True,
    errors="coerce"
)

df = df.dropna(subset=["date_of_shipment"]).reset_index(drop=True)

df["year"] = df["date_of_shipment"].dt.year.astype("Int64")
df["month"] = df["date_of_shipment"].dt.month.astype("Int64")

output_path = Path("../../data/processed/trade_intermediate.xlsx")
df.to_excel(output_path, index=False)

print("Cleaned Excel saved to:", output_path)
