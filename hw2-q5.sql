## Question 5 (6 rows)
SELECT c.name AS name, SUM(f.canceled*1.0)/COUNT(c.cid*1.0)*100 AS percentage
FROM FLIGHTS f, CARRIERS c
WHERE f.origin_city = 'Seattle WA' AND
			c.cid = f.carrier_id
GROUP BY c.name
HAVING percentage > 0.5
ORDER BY percentage ASC;