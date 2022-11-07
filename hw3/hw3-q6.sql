/*
- # of rows: 4
- The query took: 1s
- Output:
Alaska Airlines Inc.
SkyWest Airlines Inc.
United Air Lines Inc.
Virgin America
*/

SELECT c.name AS carrier
FROM Carriers c
WHERE c.cid IN (SELECT DISTINCT f.carrier_id
			    FROM Flights f
			    WHERE f.origin_city = 'Seattle WA' AND
				      f.dest_city = 'San Francisco CA')
ORDER BY carrier ASC