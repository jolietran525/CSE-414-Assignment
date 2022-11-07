## Question 3 (1 row)
SELECT f.day_of_week_id AS day_of_week, AVG(f.arrival_delay) AS delay
FROM FLIGHTS f
GROUP BY f.day_of_week_id
ORDER BY AVG(f.arrival_delay) DESC
LIMIT 1;