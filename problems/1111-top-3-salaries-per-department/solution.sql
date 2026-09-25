-- your query
SELECT department, name, salary, rnk
FROM (
    SELECT department, name, salary,
        DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk 
    FROM employees
) ranked
WHERE rnk <=3
ORDER BY department, salary DESC, name;