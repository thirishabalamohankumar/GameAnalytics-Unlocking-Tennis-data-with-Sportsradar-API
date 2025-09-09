SELECT v.venue_name, c.complex_name
FROM venues v
JOIN complexes c ON v.complex_id = c.complex_id;

SELECT c.complex_name, COUNT(v.venue_id) AS venue_count
FROM venues v
JOIN complexes c ON v.complex_id = c.complex_id
GROUP BY c.complex_name
ORDER BY venue_count DESC;

SELECT v.venue_name, v.city_name, v.country_name, c.complex_name
FROM venues v
JOIN complexes c ON v.complex_id = c.complex_id
WHERE v.country_name = 'Chile';

SELECT venue_name, timezone
FROM venues;

SELECT venue_name, timezone
FROM venues;

SELECT c.complex_name, COUNT(v.venue_id) AS venue_count
FROM complexes c
JOIN venues v ON v.complex_id = c.complex_id
GROUP BY c.complex_name
HAVING COUNT(v.venue_id) > 1;

SELECT country_name, COUNT(venue_id) AS venue_count
FROM venues
GROUP BY country_name
ORDER BY venue_count DESC;

SELECT v.venue_name, v.city_name, v.country_name
FROM venues v
JOIN complexes c ON v.complex_id = c.complex_id
WHERE c.complex_name = 'Nacional';
