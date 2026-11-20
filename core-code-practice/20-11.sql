CREATE TABLE emp (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    dept VARCHAR(50),
    salary DECIMAL(10,2),
    mgr INT,
    email VARCHAR(100),
    FOREIGN KEY (mgr) REFERENCES emp(id)
);

INSERT INTO emp (id, name, dept, salary, mgr, email)
VALUES
(1, 'Ali',   'IT',      90000, NULL, 'ali@mail.com'),
(2, 'Sara',  'IT',     100000, 1,    'sara@mail.com'),
(3, 'John',  'IT',      80000, 1,    'sara@mail.com'),
(4, 'Mary',  'HR',      70000, NULL, 'mary@mail.com'),
(5, 'Zoya',  'HR',      60000, 4,    'zoya@mail.com'),
(6, 'Ahmed', 'Sales',   50000, NULL, 'ahmed@mail.com'),
(7, 'Sam',   'Sales',   50000, 6,    'sam@mail.com'),
(8, 'Eva',   'Finance', 75000, NULL, 'eva@mail.com');

CREATE TABLE dept (
    dept VARCHAR(50) PRIMARY KEY
);

INSERT INTO dept (dept)
VALUES
('IT'),
('HR'),
('Sales'),
('Finance'),
('Marketing');

CREATE TABLE s (
    region VARCHAR(50),
    month VARCHAR(10),
    amt DECIMAL(10,2)
);

INSERT INTO s (region, month, amt)
VALUES
('North', 'Jan', 100),
('North', 'Feb', 200),
('North', 'Mar', 150),
('South', 'Jan', 50),
('South', 'Feb', 100);

SELECT * FROM emp;

SELECT * FROM dept;

SELECT * FROM s;

/*
output:
+----+-------+---------+-----------+------+----------------+
| id | name  | dept    | salary    | mgr  | email          |
+----+-------+---------+-----------+------+----------------+
|  1 | Ali   | IT      |  90000.00 | NULL | ali@mail.com   |
|  2 | Sara  | IT      | 100000.00 |    1 | sara@mail.com  |
|  3 | John  | IT      |  80000.00 |    1 | sara@mail.com  |
|  4 | Mary  | HR      |  70000.00 | NULL | mary@mail.com  |
|  5 | Zoya  | HR      |  60000.00 |    4 | zoya@mail.com  |
|  6 | Ahmed | Sales   |  50000.00 | NULL | ahmed@mail.com |
|  7 | Sam   | Sales   |  50000.00 |    6 | sam@mail.com   |
|  8 | Eva   | Finance |  75000.00 | NULL | eva@mail.com   |
+----+-------+---------+-----------+------+----------------+
+-----------+
| dept      |
+-----------+
| Finance   |
| HR        |
| IT        |
| Marketing |
| Sales     |
+-----------+
+--------+-------+--------+
| region | month | amt    |
+--------+-------+--------+
| North  | Jan   | 100.00 |
| North  | Feb   | 200.00 |
| North  | Mar   | 150.00 |
| South  | Jan   |  50.00 |
| South  | Feb   | 100.00 |
+--------+-------+--------+
*/

-- SECOND HIGHEST salary
SELECT DISTINCT salary
FROM emp
ORDER BY salary DESC
LIMIT 1 OFFSET 1;
/*
output:
+----------+
| salary   |
+----------+
| 90000.00 |
+----------+
*/

-- Groups filtered after grouping
SELECT dept, COUNT(*)
FROM emp
GROUP BY dept
HAVING AVG(salary) > 65000;
/*
output:
+---------+----------+
| dept    | COUNT(*) |
+---------+----------+
| IT      |        3 |
| Finance |        1 |
+---------+----------+
*/

-- Departments with no employees
SELECT d.dept
FROM dept d
LEFT JOIN emp e ON e.dept=d.dept
WHERE e.id IS NULL;

/*
output:
+-----------+
| dept      |
+-----------+
| Marketing |
+-----------+
*/

-- Duplicate emails
SELECT email, count(*)
FROM emp
GROUP BY email
HAVING COUNT(*)>1;

/*
output:
+---------------+----------+
| email         | count(*) |
+---------------+----------+
| sara@mail.com |        2 |
+---------------+----------+
*/

-- Employees earning more than their managers
SELECT e.name
FROM emp e
JOIN emp m ON e.mgr=m.id
WHERE e.salary>m.salary;
/*
output:
+------+
| name |
+------+
| Sara |
+------+
*/

-- Running total per region
SELECT region, month,
        SUM(amt) OVER (
          PARTITION BY region
          ORDER BY month
          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS running_total
FROM s;
/*
output:
+--------+-------+---------------+
| region | month | running_total |
+--------+-------+---------------+
| North  | Feb   |        200.00 |
| North  | Jan   |        300.00 |
| North  | Mar   |        450.00 |
| South  | Feb   |        100.00 |
| South  | Jan   |        150.00 |
+--------+-------+---------------+
*/

-- Top salary per department (ties kept)
SELECT dept, name, salary
FROM (
  SELECT dept, name, salary,
  DENSE_RANK() OVER(
    PARTITION BY dept
    ORDER BY salary DESC 
  ) rk
  FROM emp
  )ranked
  WHERE rk = 1;
/*
output:
+---------+-------+-----------+
| dept    | name  | salary    |
+---------+-------+-----------+
| Finance | Eva   |  75000.00 |
| HR      | Mary  |  70000.00 |
| IT      | Sara  | 100000.00 |
| Sales   | Ahmed |  50000.00 |
| Sales   | Sam   |  50000.00 |
+---------+-------+-----------+
*/
 

/*
Quick revision: SQL concepts you're using
SQL concept	Purpose
DISTINCT	Remove duplicates
ORDER BY	Sort records
LIMIT / OFFSET	Control returned rows
GROUP BY	Group similar records
HAVING	Filter groups
LEFT JOIN	Keep all records from the left table
IS NULL	Find missing matches
SELF JOIN	Join a table with itself
OVER()	Perform calculations without collapsing rows
PARTITION BY	Divide rows into separate groups for window calculations
DENSE_RANK()	Rank records while keeping ties
*/
