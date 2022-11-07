/*
- # of rows: 4
- The query took: 36s
- Output:
Devils Lake ND
Hattiesburg/Laurel MS
Seattle WA
St. Augustine FL
*/

SELECT DISTINCT f.dest_city AS city
FROM Flights f
WHERE f.dest_city NOT IN (SELECT DISTINCT f2.dest_city AS city
						  FROM Flights f1, Flights f2
						  WHERE f1.dest_city = f2.origin_city AND
	  							f1.origin_city = 'Seattle WA' AND
	  							f2.dest_city != 'Seattle WA' AND
	 						    f2.dest_city NOT IN (SELECT f3.dest_city
	  					   							 FROM Flights f3
						   							 WHERE f3.origin_city = 'Seattle WA')) AND
	  f.dest_city NOT IN (SELECT f3.dest_city
	  					  FROM Flights f3
						  WHERE f3.origin_city = 'Seattle WA')
ORDER BY city ASC