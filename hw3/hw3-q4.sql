/*
- # of rows: 256
- The query took: 15s
- First 20 rows:
Aberdeen SD
Abilene TX
Adak Island AK
Aguadilla PR
Akron OH
Albany GA
Albany NY
Alexandria LA
Allentown/Bethlehem/Easton PA
Alpena MI
Amarillo TX
Appleton WI
Arcata/Eureka CA
Asheville NC
Ashland WV
Aspen CO
Atlantic City NJ
Augusta GA
Bakersfield CA
Bangor ME
*/

SELECT DISTINCT f2.dest_city AS city
FROM Flights f1, Flights f2
WHERE f1.dest_city = f2.origin_city AND
	  f1.origin_city = 'Seattle WA' AND
	  f2.dest_city != 'Seattle WA' AND
	  f2.dest_city NOT IN (SELECT f3.dest_city
	  					   FROM Flights f3
						   WHERE f3.origin_city = 'Seattle WA')
ORDER BY city ASC
