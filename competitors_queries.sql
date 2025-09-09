SELECT c.name, r.rank, r.points
FROM competitors c
JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
ORDER BY r.rank ASC;

SELECT c.name, r.rank, r.points
FROM competitors c
JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
WHERE r.rank <= 5
ORDER BY r.rank ASC;

SELECT c.name, r.rank, r.movement
FROM competitors c
JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
WHERE r.movement = 0;

SELECT c.country, SUM(r.points) AS total_points
FROM competitors c
JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
WHERE c.country = 'Croatia'
GROUP BY c.country;

SELECT c.country, COUNT(c.competitor_id) AS competitor_count
FROM competitors c
GROUP BY c.country
ORDER BY competitor_count DESC;

SELECT c.name, r.rank, r.points
FROM competitors c
JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
ORDER BY r.points DESC
LIMIT 1;
