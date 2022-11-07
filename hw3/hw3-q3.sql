/*
- # of rows: 327
- The query took: 7s
- First 20 rows:
Guam TT, 0
Pago Pago TT, 0
Aguadilla PR, 28.8973384030418
Anchorage AK, 31.8120805369128
San Juan PR, 33.6605316973415
Charlotte Amalie VI, 39.5588235294118
Ponce PR, 40.9836065573771
Fairbanks AK, 50.1165501165501
Kahului HI, 53.5144713526285
Honolulu HI, 54.7390288236822
San Francisco CA, 55.8288645371882
Los Angeles CA, 56.0808908229873
Seattle WA, 57.6093877922314
Long Beach CA, 62.1764395139989
New York NY, 62.371834136728
Kona HI, 63.1607929515419
Las Vegas NV, 64.9202563720376
Christiansted VI, 65.1006711409396
Newark NJ, 65.8499710969808
Plattsburgh NY, 66.6666666666667
*/

SELECT g1.origin_city, ISNULL((g2.lessthan3 * 100 / g1.departed ), 0) AS percentage
FROM (  SELECT f1.origin_city, CAST(COUNT(f1.origin_city) AS FLOAT) AS departed
		FROM Flights f1
		WHERE f1.canceled = 0
		GROUP BY f1.origin_city ) g1
LEFT OUTER JOIN
( SELECT f2.origin_city, CAST(COUNT(f2.origin_city) AS FLOAT) AS lessthan3
  FROM Flights f2
  WHERE f2.canceled = 0 AND	
		f2.actual_time < 180
  GROUP BY f2.origin_city ) g2
ON g1.origin_city = g2.origin_city
ORDER BY percentage, origin_city ASC