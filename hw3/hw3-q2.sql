/*
- # of rows: 109
- The query took: 5s
- First 20 rows:
Aberdeen SD
Abilene TX
Alpena MI
Ashland WV
Augusta GA
Barrow AK
Beaumont/Port Arthur TX
Bemidji MN
Bethel AK
Binghamton NY
Brainerd MN
Bristol/Johnson City/Kingsport TN
Butte MT
Carlsbad CA
Casper WY
Cedar City UT
Chico CA
College Station/Bryan TX
Columbia MO
Columbus GA
*/

SELECT DISTINCT f.origin_city AS city
FROM Flights f
WHERE f.canceled = 0 AND 
	  180 > ALL ( SELECT f1.actual_time
	  			FROM Flights f1 
				WHERE f1.origin_city = f.origin_city )
ORDER BY f.origin_city ASC