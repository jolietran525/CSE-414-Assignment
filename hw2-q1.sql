.mode column
.header on

## Question 1 (3 rows)
SELECT DISTINCT f.flight_num AS flight_num
FROM FLIGHTS f, CARRIERS c
WHERE f.origin_city = 'Seattle WA' AND
      f.dest_city = 'Boston MA' AND
      f.day_of_week_id = 1 AND
      c.cid = f.carrier_id AND
      c.name = 'Alaska Airlines Inc.';