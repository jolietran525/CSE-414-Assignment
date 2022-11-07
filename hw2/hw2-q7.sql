## Question 7 (1 row)
SELECT SUM(f.capacity) AS capacity
FROM FLIGHTS f
WHERE f.month_id = 7 AND
      f.day_of_month = 10 AND
      ((f.origin_city = 'Seattle WA' AND
      f.dest_city = 'San Francisco CA') OR
      (f.origin_city = 'San Francisco CA' AND
      f.dest_city = 'Seattle WA'));
