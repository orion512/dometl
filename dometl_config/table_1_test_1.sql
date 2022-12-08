SELECT id, col1
FROM table_1 g
WHERE
	...
GROUP BY id, col1
HAVING COUNT(*) > 4