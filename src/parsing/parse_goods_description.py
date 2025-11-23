
import pandas as pd
from pathlib import Path
import numpy as np

# Input Excel file (processed earlier)
IN = Path(__file__).resolve().parents[2] / "data" / "processed" / "trade_cleaned_costs.xlsx"
OUT = Path(__file__).resolve().parents[2] / "data" / "processed" / "trade_features.xlsx"

# Simple USD → INR static conversion (optional)
USD_TO_INR = 83.0

# Category keyword mapping
CATEGORY_KEYWORDS = {
    'Glass': ['GLASS', 'BOROSILICATE', 'OPAL'],
    'Wooden': ['WOOD', 'WOODEN'],
    'Steel': ['STEEL', 'STAINLESS', 'SS'],
    'Plastic': ['PLASTIC', 'PVC'],
    'Polyhouse': ['POLYHOUSE'],
    'Ceramic': ['CERAMIC']
}

def assign_category(desc, hsn_desc=""):
    txt = f"{str(desc)} {str(hsn_desc)}".upper()
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw in txt:
                return cat
    return "Others"

def standardize_unit(u):
    if not isinstance(u, str):
        return None
    u2 = u.strip().upper()

    unit_map = {
        "PCS": "PCS",
        "PC": "PCS",
        "NOS": "PCS",
        "PIECES": "PCS",
        "PIECE": "PCS",
        "PCS.": "PCS",
        "NOS.": "PCS",
        "KG": "KG",
        "KGS": "KG",
        "KILOGRAM": "KG",
        "MT": "MT",
        "MTS": "MT",
        "TON": "MT",
        "TONNE": "MT"
    }

    return unit_map.get(u2, u2)

def compute_features(df):

    # FIXED: Using actual column names
    df['TOTAL VALUE_INR'] = pd.to_numeric(df.get('TOTAL VALUE_INR', 0), errors='coerce').fillna(0)
    df['DUTY PAID_INR'] = pd.to_numeric(df.get('DUTY PAID_INR', 0), errors='coerce').fillna(0)
    df['QUANTITY'] = pd.to_numeric(df.get('QUANTITY', 0), errors='coerce').fillna(0)

    # Grand Total
    df['grand_total_inr'] = df['TOTAL VALUE_INR'] + df['DUTY PAID_INR']

    # Standardize Units
    df['unit_standardized'] = df['UNIT'].apply(standardize_unit)

    # Landed Cost Per Unit
    df['landed_cost_per_unit_inr'] = df.apply(
        lambda r: (r['grand_total_inr'] / r['QUANTITY']) if r['QUANTITY'] > 0 else np.nan,
        axis=1
    )

    # Category assignment
    df['category'] = df.apply(
        lambda r: assign_category(r.get('GOODS DESCRIPTION', ''), ''),
        axis=1
    )

    # Duty % of value
    df['duty_pct_of_value'] = df.apply(
        lambda r: (r['DUTY PAID_INR'] / r['TOTAL VALUE_INR'])
        if r['TOTAL VALUE_INR'] > 0 else np.nan,
        axis=1
    )

    # USD → INR conversion (optional)
    df['UNIT PRICE_USD'] = pd.to_numeric(df.get('UNIT PRICE_USD', None), errors='coerce')
    df['unit_price_usd_to_inr'] = df['UNIT PRICE_USD'].apply(
        lambda x: x * USD_TO_INR if pd.notna(x) else np.nan
    )

    return df


# --------------------------
# MAIN SCRIPT
# --------------------------

if __name__ == "__main__":
    print("Loading:", IN)

    df = pd.read_excel(IN)
    print("Rows:", len(df))

    df = compute_features(df)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(OUT, index=False)

    print("\nSaved features file to:", OUT)
    print("Feature extraction completed successfully!")
