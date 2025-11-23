-- schema.sql: replicate for a proper RDBMS if you wish
-- In SQLite the table will be created automatically by pandas.to_sql. Use this for Postgres.
CREATE TABLE shipments (
    id SERIAL PRIMARY KEY,
    date_of_shipment DATE,
    year INT,
    month INT,
    quarter TEXT,
    "HSN Code" TEXT,
    "HSN Description" TEXT,
    "Goods Description" TEXT,
    "Quantity" NUMERIC,
    "Unit" TEXT,
    "Unit Price (INR)" NUMERIC,
    "Total Value (INR)" NUMERIC,
    "Duty Paid (INR)" NUMERIC,
    supplier_name TEXT,
    supplier_address TEXT,
    model_extracted TEXT,
    capacity_extracted TEXT,
    material_extracted TEXT,
    embedded_quantity INT,
    unit_price_usd_extracted NUMERIC,
    unit_standardized TEXT,
    grand_total_inr NUMERIC,
    landed_cost_per_unit_inr NUMERIC,
    category TEXT,
    duty_pct_of_value NUMERIC
);
