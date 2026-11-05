-- your query
SELECT department, employee, score,
ROW_NUMBER() OVER (PARTITION BY department ORDER BY score DESC, employee ASC) as rn,
RANK() OVER (PARTITION BY department ORDER BY score DESC) as rnk,
DENSE_RANK() OVER (PARTITION BY department ORDER BY score DESC) as dense_rnk
FROM scores
ORDER BY 
department ASC,
score DESC,
employee ASC;