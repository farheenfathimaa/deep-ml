select (
  SELECT DISTINCT salary
  FROM employee
  ORDER BY salary DESC
  LIMIT 1 OFFSET 2
) as nth_salary;