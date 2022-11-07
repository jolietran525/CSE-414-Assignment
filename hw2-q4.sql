## Question 4 (12 rows)
SELECT DISTINCT c.name AS name
FROM FLIGHTS f, CARRIERS c
WHERE f.carrier_id = c.cid
GROUP BY c.name, f.month_id, f.day_of_month
HAVING COUNT(f.fid) > 1000;