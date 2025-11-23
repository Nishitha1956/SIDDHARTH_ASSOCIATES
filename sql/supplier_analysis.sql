WITH supplier_years AS (
  SELECT supplier_name, year, COUNT(*) AS cnt FROM shipments GROUP BY supplier_name, year
)
SELECT s.supplier_name,
       MAX(CASE WHEN sy.year = 2025 THEN 1 ELSE 0 END) AS active_2025,
       SUM(CASE WHEN sy.year < 2025 THEN 1 ELSE 0 END) AS shipments_before_2025
FROM (SELECT DISTINCT supplier_name FROM shipments) s
LEFT JOIN supplier_years sy ON sy.supplier_name = s.supplier_name
GROUP BY s.supplier_name
ORDER BY active_2025 DESC, shipments_before_2025 DESC;
