import pandas as pd
import mysql.connector
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]
IN = BASE_DIR / "data" / "processed" / "trade_cleaned_costs.xlsx"

def load_to_mysql(excel_path=IN):

    if not excel_path.exists():
        raise FileNotFoundError(f"❌ Input file not found: {excel_path}")

    print(f"📄 Loading Excel file: {excel_path}")

    df = pd.read_excel(excel_path)
    print(f"✔ Loaded {len(df)} rows and {len(df.columns)} columns.")

    # Replace NaN with None for MySQL
    df = df.replace({np.nan: None})

    # EXACT columns from the Excel file
    expected_columns = [
        'PORT CODE',
        'DATE',
        'IEC',
        'HS CODE',
        'GOODS DESCRIPTION',
        'Master category',
        'Model Name',
        'Model Number',
        'Capacity',
        'Qty',
        'Unit of measure',
        'Price',
        'Unit of measure.1',
        'QUANTITY',
        'UNIT',
        'UNIT PRICE_INR',
        'TOTAL VALUE_INR',
        'UNIT PRICE_USD',
        'TOTAL VALUE_USD',
        'DUTY PAID_INR'
    ]

    # Check missing columns
    missing = [col for col in expected_columns if col not in df.columns]
    if missing:
        raise Exception(f"❌ ERROR: Missing columns in Excel: {missing}")

    # Reorder columns correctly
    df = df[expected_columns]

    print("🔌 Connecting to MySQL...")

    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Nishuv#41",
        database="trade_analysis"
    )
    cursor = conn.cursor()
    print("✔ Connected to MySQL.")

    insert_query = """
        INSERT INTO shipments (
            port_code, date, iec, hs_code, goods_description, master_category,
            model_name, model_number, capacity, qty, unit_of_measure, price,
            unit_of_measure_1, quantity, unit, unit_price_inr, total_value_inr,
            unit_price_usd, total_value_usd, duty_paid_inr
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    print("📥 Inserting rows...")

    for _, row in df.iterrows():
        cursor.execute(insert_query, tuple(row[col] for col in expected_columns))

    conn.commit()
    conn.close()

    print("🎉 SUCCESS! Data loaded into MySQL table `shipments`.")

if __name__ == "__main__":
    load_to_mysql()
