WITH hsn_totals AS (
  SELECT "HSN Code" AS hsn_code, SUM("Total Value (INR)") AS total_value_inr
  FROM shipments
  GROUP BY "HSN Code"
),
total_sum AS (SELECT SUM(total_value_inr) AS grand_sum FROM hsn_totals),
ranked AS (
  SELECT hsn_code, total_value_inr,
         ROW_NUMBER() OVER (ORDER BY total_value_inr DESC) AS rn
  FROM hsn_totals
)
SELECT CASE WHEN rn <= 25 THEN hsn_code ELSE 'OTHERS' END AS hsn_bucket,
       SUM(total_value_inr) AS bucket_value,
       SUM(total_value_inr) * 100.0 / (SELECT grand_sum FROM total_sum) AS pct_of_total
FROM ranked
GROUP BY CASE WHEN rn <= 25 THEN hsn_code ELSE 'OTHERS' END
ORDER BY bucket_value DESC;
