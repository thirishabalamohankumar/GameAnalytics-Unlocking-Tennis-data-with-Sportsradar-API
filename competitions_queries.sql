SELECT c.competition_name, cat.category_name
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id;

SELECT cat.category_name, COUNT(c.competition_id) AS competition_count
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name
ORDER BY competition_count DESC;

SELECT competition_name, type, gender
FROM competitions
WHERE type = 'doubles';

SELECT c.competition_name, cat.category_name
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';

SELECT parent.competition_name AS parent_competition,
       child.competition_name AS sub_competition
FROM competitions child
JOIN competitions parent 
  ON child.parent_id = parent.competition_id
ORDER BY parent.competition_name;

SELECT cat.category_name, c.type, COUNT(*) AS competition_count
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type
ORDER BY cat.category_name, c.type;

SELECT competition_name, type, gender
FROM competitions
WHERE parent_id IS NULL;
