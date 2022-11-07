## Question 8 (22 rows)
SELECT c.name AS name, SUM(f.departure_delay) AS delay
FROM FLIGHTS f , CARRIERS c
WHERE c.cid = f.carrier_id
GROUP BY c.name;