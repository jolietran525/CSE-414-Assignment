/*
- # of rows: 334
- The query took: 12s
- First 20 rows:
Aberdeen SD, Minneapolis MN, 106
Abilene TX, Dallas/Fort Worth TX, 111
Adak Island AK, Anchorage AK, 471
Aguadilla PR, New York NY, 368
Akron OH, Atlanta GA, 408
Albany GA, Atlanta GA, 243
Albany NY, Atlanta GA, 390
Albuquerque NM, Houston TX, 492
Alexandria LA, Atlanta GA, 391
Allentown/Bethlehem/Easton PA, Atlanta GA, 456
Alpena MI, Detroit MI, 80
Amarillo TX, Houston TX, 390
Anchorage AK, Barrow AK, 490
Appleton WI, Atlanta GA, 405
Arcata/Eureka CA, San Francisco CA, 476
Asheville NC, Chicago IL, 279
Ashland WV, Cincinnati OH, 84
Aspen CO, Los Angeles CA, 304
Atlanta GA, Honolulu HI, 649
Atlantic City NJ, Fort Lauderdale FL, 212
*/

WITH MaxTime AS
	( SELECT f1.origin_city, MAX(f1.actual_time) AS time
	  FROM Flights f1
	  GROUP BY f1.origin_city )
SELECT DISTINCT f2.origin_city AS origin_city, f2.dest_city AS dest_city, f2.actual_time AS time
FROM Flights f2, MaxTime mt
WHERE f2.origin_city = mt.origin_city AND
	  f2.actual_time = mt.time
ORDER BY f2.origin_city, f2.dest_city ASC