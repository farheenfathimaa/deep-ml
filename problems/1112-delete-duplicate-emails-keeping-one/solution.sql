-- your query
SELECT MIN(id) AS id, email 
from person 
group by email
ORDER BY id; 
